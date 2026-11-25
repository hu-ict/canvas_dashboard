import statistics

import numpy as np
from scripts.model.learning_outcome.SaturationLearningOutcome import SaturationLearningOutcome
from scripts.model.learning_outcome.SaturationPortfolioItem import SaturationPortfolioItem
from scripts.model.learning_outcome.SaturationStatistics import SaturationStatistics

def get_y_max(results):
    all_high = 0
    for saturation_learning_outcome in results.saturation_learning_outcomes:
        high = saturation_learning_outcome.get_day(results.actual_day).high
        if high > all_high:
            all_high = high
    return all_high

def get_bof_value(a_course, a_results, a_workload):
    for student in a_course.students:
        for assessor in student.assessors:
            teacher = a_workload.get_dimension("teachers").get_workload_item(assessor.teacher_id)
            assignment_group = a_course.get_assignment_group(assessor.assignment_group_id)
            for assignment_sequence in assignment_group.assignment_sequences:
                for assignment in assignment_sequence.assignments:
                    if assignment.day <= a_results.actual_day:
                        teacher.total_value += assignment.points
    for student in a_results.students:
        for learning_outcome in student.learning_outcomes.values():
            for feedback in learning_outcome.feedback_list:
                teacher = a_workload.get_dimension("teachers").get_workload_item(feedback.author_id)
                if teacher is not None:
                    teacher.bof_count += 1
                else:
                    print("BTW91 - teacher not found", feedback.author_id, feedback.author_name )
    return a_workload

def get_bof_saturation(a_course, a_results):
    # aanmaken structuur
    a_results.saturation_learning_outcomes = []
    for learning_outcome in a_course.learning_outcomes:
        saturation_learning_outcome = SaturationLearningOutcome(learning_outcome_id=learning_outcome.id, short=learning_outcome.short)
        a_results.saturation_learning_outcomes.append(saturation_learning_outcome)
        for day in range(a_results.actual_day+1):
            saturation_learning_outcome.days.append(SaturationStatistics(learning_outcome_id=learning_outcome.id, short=learning_outcome.short, day=day, low=0, min_stdv=0, average=0, plus_stdv=0, high=0 ))
    print("LIBSAT21 - learning_outcome count", len(a_results.saturation_learning_outcomes))
    # collectie vullen vanuit studenten
    for student in a_results.students:
        for learning_outcome in student.learning_outcomes.values():
            saturation_day_list = learning_outcome.get_saturation_day_list(a_results.actual_day)
            for day in saturation_day_list:
                l_day = a_results.get_learning_outcome(learning_outcome.id).get_day(day.day)
                l_day.collection.append(day.value)

    # bepaal de statistiek per learning_outcome en day
    for learning_outcome in a_results.saturation_learning_outcomes:
        for day in learning_outcome.days:
            if len(day.collection) > 0:
                day.average = round(sum(day.collection)/len(day.collection), 2)
                stdv = statistics.stdev(day.collection)
                day.low = min(day.collection)
                day.high = max(day.collection)
                plus_stdv = day.average + stdv
                min_stdv = day.average - stdv
                if min_stdv < 0:
                    min_stdv = 0
                day.plus_stdv = round(plus_stdv, 2)
                day.min_stdv = round(min_stdv, 2)
            # percentile_25 = np.percentile(learning_outcomes[learning_outcome.id]['day_list'][day]["collection"], 75)
            # percentile_50 = np.percentile(learning_outcomes[learning_outcome.id]['day_list'][day]["collection"], 50)
            # percentile_75 = np.percentile(learning_outcomes[learning_outcome.id]['day_list'][day]["collection"], 25)
        learning_outcome.last_day_collection = learning_outcome.days[-1].collection

def get_relative_saturation(learning_outcome, student_learning_outcome, actual_day):
    value = student_learning_outcome['day_list'][actual_day]['value']
    min_stdv = learning_outcome['day_list'][actual_day]['min_stdv']
    if value < min_stdv:
        return False
    else:
        return True

def get_student_saturations(a_results):
    student_saturation = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0}
    for student in a_results.students:
        student_saturation[str(student.get_saturation_level())] += 1
    return student_saturation

def get_portfolio_saturation(course, results):
    portfolio_items = {}
    for assignment_group in course.assignment_groups:
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                if assignment.unlock_day <= results.actual_day:
                    portfolio_items[assignment.id] = SaturationPortfolioItem(assignment.id, assignment.name, assignment.day)
    for student in results.students:
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    count = 0
                    for learning_outcome in submission.learning_outcomes.values():
                        count += len(learning_outcome.feedback_list)
                    portfolio_items[submission.assignment.id].collection.append(count)
    gesorteerd = dict(
        sorted(portfolio_items.items(),
               key=lambda item: (item[1].day))
    )
    return gesorteerd

def get_teacher_portfolio_saturations(teacher_id, course, results, portfolio_saturations):
    teacher_portfolio_items = {}
    for assignment_group in course.assignment_groups:
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                if assignment.unlock_day <= results.actual_day:
                    if course.is_responsible(teacher_id, assignment.group_id):
                        teacher_portfolio_items[assignment.id] = SaturationPortfolioItem(assignment.id, assignment.name, assignment.day)
    for student in results.students:
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    course_student = course.find_student(student.id)
                    # print("LIBSAT31 -", course_student.name, course_student.is_assessor(teacher_id, submission.assignment.group_id))
                    if course_student.is_assessor(teacher_id, submission.assignment.group_id):
                        count = 0
                        for learning_outcome in submission.learning_outcomes.values():
                            count += len(learning_outcome.feedback_list)
                        teacher_portfolio_items[submission.assignment.id].collection.append(count)
    for teacher_portfolio_item in teacher_portfolio_items:
        teacher_average_lu = teacher_portfolio_items[teacher_portfolio_item].get_average_lu()
        portfolio_item_average_lu = portfolio_saturations[teacher_portfolio_item].get_average_lu()

    gesorteerd = dict(
        sorted(teacher_portfolio_items.items(),
               key=lambda item: (item[1].day))
    )
    return gesorteerd


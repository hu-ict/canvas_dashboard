from scripts.model.perspective.Status import NOT_YET_GRADED, NOT_CORRECT_GRADED
from scripts.model.workload.Workload import Workload
from scripts.model.workload.WorkloadDimension import WorkloadDimension
from scripts.model.workload.WorkloadItem import WorkloadItem


def get_teachers(course):
    teachers = set()
    for teacher in course.teachers:
        if teacher in teachers:
            pass
        else:
            if len(teacher.responsibilities) > 0:
                teachers.add(teacher)
    teacher_list = list(teachers)
    teacher_list = sorted(teacher_list, key=lambda t: t.initials)
    return teacher_list


def create_workload(dashboard, teachers, groups_1, groups_2):
    workload = Workload(1)
    workload_dimension = WorkloadDimension("teachers", "Docent")
    for teacher in teachers:
        workload_dimension.items.append(WorkloadItem(teacher.id, teacher.initials, teacher.name, 0,0,0, 0, 0))
    workload_dimension.items = sorted(workload_dimension.items, key=lambda t: t.short)
    workload.dimensions.append(workload_dimension)

    workload_dimension = WorkloadDimension("groups_1", dashboard.groups_1.title)
    for group in groups_1:
        workload_dimension.items.append(WorkloadItem(group.id, group.name, group.name, 0,0,0, 0, 0))
    workload_dimension.items = sorted(workload_dimension.items, key=lambda t: t.short)
    workload.dimensions.append(workload_dimension)

    workload_dimension = WorkloadDimension("groups_2", dashboard.groups_2.title)
    for group in groups_2:
        workload_dimension.items.append(WorkloadItem(group.id, group.name, group.name, 0, 0, 0, 0, 0))
    workload_dimension.items = sorted(workload_dimension.items, key=lambda t: t.short)
    workload.dimensions.append(workload_dimension)
    return workload

def find_teacher(teachers, teacher_id):
    for teacher in teachers:
        if teacher.id == teacher_id:
            return teacher
    return None

def student_total(a_perspective):
    cum_score = 0
    for submission_sequence in a_perspective.submission_sequences:
        cum_score += submission_sequence.get_score()
    return cum_score


def add_total(totals, total):
    totals.append(total)


def get_submitted_at(item):
    return item.submitted_at


def check_for_late(a_course, a_submission, a_workload, a_actual_day):
    if a_submission.status == NOT_YET_GRADED or a_submission.status == NOT_CORRECT_GRADED:
        student = a_course.find_student(a_submission.student_id)
        if student:
            if a_submission.submitted_day is None:
                late_days = a_actual_day - a_submission.assignment.day
            else:
                late_days = a_actual_day - a_submission.submitted_day
            for dimension in a_workload.dimensions:
                if dimension.name == "teachers":
                    assessor = student.get_assessor_by_assignment_group(a_submission.assignment.group_id)
                    if assessor is None:
                        print("BTW81 - No assessor for assignment.group_id", a_submission.assignment.group_id,
                              student.name)
                        break
                    item_id = assessor.teacher_id
                elif dimension.name == "groups_1":
                    item_id = student.groups_1_group_id
                    if item_id == 0:
                        print("BTW82 - No groups_1 for student", student.groups_1_group_id, student.name)
                        break
                elif dimension.name == "groups_2":
                    item_id = student.groups_2_group_id
                    if item_id == 0:
                        print("BTW83 - No groups_2 for student", student.groups_2_group_id, student.name)
                        break
                else:
                    print("BTW84 - Unknown dimension", dimension.name)
                    break
                workload_item = dimension.get_workload_item(item_id)
                if workload_item is None:
                    print("BTW85 - Workload_item not found", item_id, student.name)
                    break
                if late_days <= 7:
                    workload_item.w1_count += 1
                elif 7 < late_days <= 14:
                    workload_item.w2_count += 1
                else:
                    workload_item.w3_count += 1
                workload_item.worklist.append(a_submission.to_json())
        else:
            print("BTW86 - Student not found: a_course.find_student(a_submission.student_id)", a_submission.student_id, a_submission.assignment.id)


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

def get_workload(a_course, a_results, a_workload):
    for student_results in a_results.students:
        for perspective in student_results.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    check_for_late(a_course, submission, a_workload, a_results.actual_day)

        for submission in student_results.student_level_moments.submissions:
            # print("BT87 -", student_results.student_level_moments.name, submission)
            # print("BT89 -", list(a_student_totals['perspectives'][student_results.student_level_moments.name]['list']))
            check_for_late(a_course, submission, a_workload, a_results.actual_day)
        for submission in student_results.student_grade_moments.submissions:
            # print("BT87 -", student_results.student_grade_moments.name, submission)
            # print("BT88 -", submission.status)
            # print("BT89 -", list(a_student_totals['perspectives'][student_results.student_level_moments.name]['list']))
            check_for_late(a_course, submission, a_workload, a_results.actual_day)
    return a_workload



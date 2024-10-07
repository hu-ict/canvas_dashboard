from lib.lib_date import get_date_time_obj, date_to_day, get_actual_date, get_date_time_str
from model.Comment import Comment
from model.CriteriumScore import CriteriumScore
from model.Submission import Submission
from random import randrange

NOT_GRADED = "Nog niet beoordeeld."
NO_SUBMISSION = "Niets ingeleverd voor de deadline"
NO_DATA = "Geen data"


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def get_submission_date(a_canvas_submission, a_start, a_assignment):
# bepaal de date/time van het datapunt
    if a_canvas_submission.submitted_at:
        submitted_date = get_date_time_obj(a_canvas_submission.submitted_at)
    else:
        submitted_date = a_assignment.assignment_date
    submitted_day = date_to_day(a_start.start_date, submitted_date)
    return submitted_date, submitted_day


def get_sum_score(a_submissions, a_start_date):
    l_sum_score = 0
    l_last_score = 0
    for submission in a_submissions:
        if submission.graded:
            l_sum_score += submission.score
            if l_last_score < date_to_day(a_start_date, submission.submitted_date):
                l_last_score = date_to_day(a_start_date, submission.submitted_date)
    return l_sum_score, l_last_score


def count_graded(results):
    l_graded = 0
    l_not_graded = 0
    for student in results.students:
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    if submission.graded:
                        l_graded += 1
                    else:
                        l_not_graded += 1
    return l_graded + l_not_graded, l_not_graded


def get_sum_score_print(a_submissions, a_start_date):
    l_sum_score = 0
    l_last_score = 0
    for submission in a_submissions:
        if submission.graded:
            l_sum_score += submission.score
            # print(submission.assignment_name, submission.score, l_sum_score)
            if l_last_score < date_to_day(a_start_date, submission.submitted_date):
                l_last_score = date_to_day(a_start_date, submission.submitted_date)
    return l_sum_score, l_last_score


def get_submitted_at(item):
    return item[1].submitted_at


def remove_assignment(a_assignments, a_submission):
    for i in range(0, len(a_assignments)):
        if a_assignments[i].id == a_submission.assignment_id:
            del a_assignments[i]
            return a_assignments
    return a_assignments


def get_rubric_score(rubrics_submission, student):
    rubric_score = 0.00
    criterium_scores = []
    error = ""
    if rubrics_submission is not None:
        for canvas_criterium in rubrics_submission:
            # print("LS40 -", canvas_criterium)
            id = canvas_criterium[0]
            points = 0
            if 'points' in canvas_criterium[1].keys():
                points = canvas_criterium[1]['points']
                rubric_score += points
            else:
                error = f"ERROR in criterium_score, student {student.name} group {student.group_id}, canvas_submission {canvas_criterium}, teacher action required."
                print("LS41 -", error)
            rating_id = canvas_criterium[1]['rating_id']
            comments = canvas_criterium[1]['comments']
            criterium_score = CriteriumScore(id, rating_id, points, comments)
            # print("LS42 -", criterium_score)
            criterium_scores.append(criterium_score)
    return criterium_scores, round(rubric_score, 2), error


def submission_builder(a_start, a_course, a_student, a_assignment, a_canvas_submission):
    errors = []
    if a_canvas_submission.grade:
        graded = True
    else:
        if a_canvas_submission.grader_id:
            graded = True
        else:
            graded = False
    canvas_comments = a_canvas_submission.submission_comments
    if not a_canvas_submission.submitted_at and len(canvas_comments) == 0 and not graded:
        return
    # print("SB05 -", graded, a_canvas_submission.grader_id)
    if not graded:
        grader_name = None
        grader_date = None
        submission_score = 0
        l_submission = Submission(a_canvas_submission.id, a_assignment.group_id, a_assignment.id, a_student.id,
                                  a_assignment.name,
                                  a_assignment.assignment_date,
                                  a_assignment.assignment_day,
                                  None,
                                  None,
                                  graded, grader_name, grader_date, submission_score,
                                  a_assignment.points, 0)
        for canvas_comment in canvas_comments:
            l_submission.comments.append(
                Comment(canvas_comment['author_id'],
                        canvas_comment['author_name'],
                        get_date_time_obj(canvas_comment['created_at']),
                        canvas_comment['comment']))
        l_submission.submitted_date, l_submission.submitted_day = get_submission_date(a_canvas_submission, a_start, a_assignment)
        return l_submission

    if len(a_assignment.rubrics) > 0:
        if hasattr(a_canvas_submission, "rubric_assessment"):
            canvas_submission_rubrics = a_canvas_submission.rubric_assessment.items()
            if len(canvas_submission_rubrics) == 0:
                canvas_submission_rubrics = None
        else:
            canvas_submission_rubrics = None
    else:
        canvas_submission_rubrics = None
    # maak een submission en voeg de commentaren toe
    # print("LS31 -", f"submission_builder [{graded}] [{a_canvas_submission.submitted_at}] grade {a_canvas_submission.grade} grader_id {a_canvas_submission.grader_id} comments {len(canvas_comments)} score {a_canvas_submission.score} grading_type {a_assignment.grading_type} and student {a_student.name}.")
    submission_score = 0.0
    if canvas_submission_rubrics is None:
        #Geen rubrics bij submission
        rubrics_scores = None
        # Geen rubriek dus voldaan niet voldaan wordt gebruikt bij bepalen score
        if len(a_assignment.rubrics) > 0:
            errors.append(f"WARNING rubrics defined in assignment [{a_assignment.name}] but not used in submission for student {a_student.name} group {a_student.group_id}. Teacher action required.")
            print("LS52 -", errors[-1])

        if a_assignment.grading_type == "pass_fail":
            if a_canvas_submission.grade == 'complete':
                submission_score = a_assignment.points
                errors = []
            elif a_canvas_submission.grade == 'incomplete':
                submission_score = round(a_assignment.points/2, 2)
            else:
                submission_score = 0.00
        elif a_assignment.grading_type == "points":
            if a_canvas_submission.score is None:
                errors.append(f"ERROR score is empty {a_canvas_submission.grade} {a_canvas_submission.grader_id} for assignment {a_assignment.name} and student {a_student.name} group {a_student.group_id}.")
                print("LS75 -", errors[-1])
                submission_score = 0.00
            else:
                submission_score = round(a_canvas_submission.score, 2)
        elif a_assignment.grading_type == "letter_grade":
            # error = f"Warning grading_type {a_assignment.grading_type} for assignment {a_assignment.name} has no rubrics for {a_student.name}."
            # print("LS81 -", a_assignment.grading_type, round(a_canvas_submission.score, 2))
            submission_score = round(a_canvas_submission.score, 2)
        else:
            errors.append(f"ERROR Unknown grading_type {a_assignment.grading_type} for assignment {a_assignment.name}")
            print("LS82 -", errors[-1])
            submission_score = round(a_canvas_submission.score, 2)
    else:
        # 'pass_fail', 'percent', 'letter_grade', 'gpa_scale', 'points'
        rubrics_scores, rubric_score, error = get_rubric_score(canvas_submission_rubrics, a_student)
        if len(error) > 0:
            errors.append(error)
        if a_assignment.grading_type == "pass_fail":
            if a_canvas_submission.score is not None:
                #INNO vd/nvd met rubrics voor de "echte" punten (verborgen voor studenten)
                if a_canvas_submission.score == 0:
                    submission_score = round(rubric_score, 2)
                else:
                    submission_score = round(a_canvas_submission.score, 2)
            else:
                submission_score = round(rubric_score, 2)
        elif a_assignment.grading_type == "letter_grade":
            submission_score = round(rubric_score, 2)
        elif a_assignment.grading_type == "points":
            if a_canvas_submission.score is not None:
                submission_score = round(a_canvas_submission.score, 2)
                if submission_score != round(rubric_score, 2):
                    if a_assignment.id == 295123:
                        # uitzondering voor opdracht CSC - MITRE ATTACK
                        submission_score = submission_score
                    else:
                        submission_score = round(rubric_score, 2)
            else:
                print(a_canvas_submission, a_canvas_submission.score)
                errors.append(f"WARNING Submission score is empty {a_assignment.grading_type} for assignment {a_assignment.name}, student: {a_student.name} group {a_student.group_id}.")
                print("LS02 -", errors)
                submission_score = 0.00
        else:
            errors.append(error = f"ERROR Unknown grading_type {a_assignment.grading_type} for assignment {a_assignment.name}")
            print("LS04 -", errors[-1])

    if len(errors) > 0:
        graded = False
    if a_canvas_submission.grader_id is not None and a_canvas_submission.grader_id > 0:
        teacher = a_course.find_teacher(a_canvas_submission.grader_id)
        if teacher:
            grader_name = teacher.name
        else:
            grader_name = a_canvas_submission.grader_id
        if a_canvas_submission.graded_at:
            grader_date = get_date_time_obj(a_canvas_submission.graded_at)
        else:
            grader_date = None
    else:
        grader_name = "Onbekend"
        grader_date = None

    l_submission = Submission(a_canvas_submission.id, a_assignment.group_id, a_assignment.id, a_student.id,
                              a_assignment.name,
                              a_assignment.assignment_date,
                              a_assignment.assignment_day,
                              None,
                              None,
                              graded, grader_name, grader_date, submission_score,
                              a_assignment.points, 0)
    for canvas_comment in canvas_comments:
        # print("LS51 -", a_student.name, canvas_comment['comment'])
        l_submission.comments.append(Comment(canvas_comment['author_id'], canvas_comment['author_name'], get_date_time_obj(canvas_comment['created_at']), remove_html_tags(canvas_comment['comment'])))
    if rubrics_scores is not None:
        l_submission.rubrics = rubrics_scores
    if len(errors) > 0:
        # er is een fout opgetreden, waarschijnlijk in de rubrics
        for error in errors:
            l_submission.comments.append(Comment(0, "Systeem", get_date_time_obj(get_date_time_str(get_actual_date())), error))

    # bepaal de date/time van het datapunt
    l_submission.submitted_date, l_submission.submitted_day = get_submission_date(a_canvas_submission, a_start, a_assignment)
    l_submission.messages = errors
    return l_submission


def add_missed_assignments(course, actual_day, perspective):
    if len(perspective.assignment_groups) == 1:
        assignment_group = course.find_assignment_group(perspective.assignment_groups[0])
        if assignment_group is None:
            print("LS06 - Assignment_group for perspective not found in course", perspective.assignment_groups[0])
            return
        # maak een deep-copy van de lijst
        for assignment_sequence in assignment_group.assignment_sequences:
            # remove already submitted
            # perspective.get_is_submitted(assignment_sequence)
            if perspective.get_submitted(assignment_sequence, actual_day) is None:
                assignment = assignment_sequence.get_last_passed_assignment(actual_day)
                if assignment is not None:
                    l_submission = Submission(0, assignment.group_id, assignment.id, 0, assignment.name,
                                              assignment.assignment_date,
                                              assignment.assignment_day,
                                              assignment.assignment_date,
                                              assignment.assignment_day,
                                              True, "System", assignment.assignment_date, 0, assignment.points, 0)
                    l_submission.comments.append(Comment(0, "System", assignment.assignment_date, NO_SUBMISSION))
                    perspective.put_submission(assignment_sequence, l_submission)
    elif len(perspective.assignment_groups) > 1:
        print("LS07 - Perspective has more then one assignment_groups attached", perspective.name,
              perspective.assignment_groups)
    else:
        print("LS08 - Perspective has no assignment_groups attached", perspective.name, perspective.assignment_groups)


def read_submissions(a_canvas_course, a_start, a_course, a_results, a_total_refresh):
    for assignment_group in a_course.assignment_groups:
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                print("LS10 - Processing Assignment {0:6} - {1} - {2}".format(assignment.id, assignment_group.name, assignment.name))
                if not a_total_refresh and ((a_results.actual_date - assignment.assignment_date).days > 10):
                    # deadline langer dan twee weken geleden. Alle feedback is gegeven.
                    continue
                if assignment.unlock_date:
                    if assignment.unlock_date > a_results.actual_date:
                        # volgende assignment
                        continue
                if (assignment.assignment_date - a_results.actual_date).days > 10:
                    # deadline ligt nog 10 dagen voor actual_date
                    continue
                canvas_assignment = a_canvas_course.get_assignment(assignment.id, include=['submissions'])
                if canvas_assignment is not None:
                    canvas_submissions = canvas_assignment.get_submissions(include=['submission_comments', 'rubric_assessment'])
                    for canvas_submission in canvas_submissions:
                        student = a_results.find_student(canvas_submission.user_id)
                        if student is not None:
                            # voeg een submission toe aan een van de perspectieven
                            # print(f"R31 Submission for {student.name}")
                            l_submission = submission_builder(a_start, a_course, student, assignment, canvas_submission)

                            if l_submission is not None:
                                l_perspective = a_course.find_perspective_by_assignment_group(l_submission.assignment_group_id)
                                if l_perspective:
                                    if l_perspective.name == "level_moments":
                                        l_submission.body = canvas_submission.body
                                        if a_total_refresh:
                                            student.student_level_moments.submissions.append(l_submission)
                                        else:
                                            student.student_level_moments.put_submission(l_submission)

                                        # print("LS18 - PERSPECTIVE level_moments")
                                    else:
                                        # print("LS19 -", student.perspectives.keys())
                                        this_perspective = student.perspectives[l_perspective.name]
                                        if this_perspective is not None:
                                            this_perspective.put_submission(assignment_sequence, l_submission)

                                else:
                                    print(f"LS21 - Warning, could not find perspective for assignment_group {assignment_group.name}")
                            # else:
                            #     print(f"R22 - Error creating submission {assignment.name} for student {student.name}")
                        # else:
                        #     print("R23 Could not find student", canvas_submission.user_id)
                else:
                    print("LS25 - Could not find assignment", canvas_assignment.id, "within group", assignment_group.id)



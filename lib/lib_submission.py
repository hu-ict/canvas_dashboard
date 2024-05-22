from lib.lib_date import get_date_time_obj, date_to_day
from model.Comment import Comment
from model.CriteriumScore import CriteriumScore
from model.Submission import Submission

NOT_GRADED = "Nog niet beoordeeld."
NO_SUBMISSION = "Niets ingeleverd voor de deadline"
NO_DATA = "Geen data"


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
            for submission in perspective.submissions:
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
    if rubrics_submission:
        # try:
            for canvas_criterium in rubrics_submission:
                # print(canvas_criterium)
                id = canvas_criterium[0]
                try:
                    points = canvas_criterium[1]['points']
                    rubric_score += points
                except:
                    print(
                        f"R41 Fout in criterium_score criterium {canvas_criterium} canvas_submission {rubrics_submission} student {student.name}")
                    points = 0.00

                rating_id = canvas_criterium[1]['rating_id']
                comments = canvas_criterium[1]['comments']
                criterium_score = CriteriumScore(id,rating_id, points, comments)
                # print(criterium_score)
                criterium_scores.append(criterium_score)
        # except:
        #     print(f"R42 Fout in bepalen rubric_score {rubrics_assessment}")
    return criterium_scores, round(rubric_score, 2)


def submission_builder(a_start, a_course, a_student, a_assignment, a_canvas_submission):
    if a_canvas_submission.grade:
        graded = True
    else:
        # print("--", a_assignment.name, a_assignment.points, a_canvas_submission.grade, "score = 0")
        score = 0.0
        if a_canvas_submission.grader_id:
            graded = True
        else:
            graded = False

    try:
        rubrics_assessment = a_canvas_submission.rubric_assessment.items()
        if len(rubrics_assessment) > 0:
            graded = True
    except:
        rubrics_assessment = None

    # maak een submission en voeg de commentaren toe
    canvas_comments = a_canvas_submission.submission_comments
    if not a_canvas_submission.submitted_at and len(canvas_comments) == 0 and not graded:
        return None
    else:
        # 'pass_fail', 'percent', 'letter_grade', 'gpa_scale', 'points'
        rubrics_scores = []
        if a_assignment.grading_type == "letter_grade" or a_assignment.grading_type == "pass_fail":
            rubrics_scores, score = get_rubric_score(rubrics_assessment, a_student)
            if a_assignment.grading_type == "pass_fail" and score == 0:
                if a_canvas_submission.grade == 'complete':
                    score = 1.0
                elif a_canvas_submission.grade == 'incomplete':
                    score = 0.0
        elif a_assignment.grading_type == "points":
            if graded:
                if a_canvas_submission.score == None:
                    print(a_canvas_submission, a_canvas_submission.score)
                    print(f"S02 WARNING Submission score is empty {a_assignment.grading_type} for assignment {a_assignment.name}, student: {a_student.name}")
                    score = 0.00
                else:
                    submission_score = round(a_canvas_submission.score, 2)

                    rubrics_scores, rubric_score = get_rubric_score(rubrics_assessment, a_student)
                    if submission_score != rubric_score:
                        if rubric_score > 0:
                            score = rubric_score
                        else:
                            score = submission_score
                    else:
                        score = submission_score
            else:
                score = 0.00
        else:
            print(f"S04 ERROR Unknown grading_type {a_assignment.grading_type} for assignment {a_assignment.name}")
        if a_canvas_submission.grader_id and a_canvas_submission.grader_id > 0:
            teacher = a_course.find_teacher(a_canvas_submission.grader_id)
            if teacher:
                grader_name = teacher.name
            else:
                grader_name = a_canvas_submission.grader_id
            if a_canvas_submission.graded_at:
                grader_date = get_date_time_obj(a_canvas_submission.graded_at)
        else:
            grader_name = "onbekend"
            grader_date = None

        l_submission = Submission(a_canvas_submission.id, a_assignment.group_id, a_assignment.id, a_student.id,
                                  a_assignment.name,
                                  a_assignment.assignment_date,
                                  date_to_day(a_start.start_date, a_assignment.assignment_date),
                                  None,
                                  None,
                                  graded, grader_name, grader_date, score,
                                  a_assignment.points, 0)
        l_submission.rubrics = rubrics_scores
        for canvas_comment in canvas_comments:
            l_submission.comments.append(
                Comment(canvas_comment['author_id'], canvas_comment['author_name'],
                        get_date_time_obj(canvas_comment['created_at']), canvas_comment['comment']))
        # bepaal de date/time van het datapunt
        if a_canvas_submission.submitted_at:
            l_submission.submitted_date = get_date_time_obj(a_canvas_submission.submitted_at)
            l_submission.submitted_day = date_to_day(a_start.start_date, l_submission.submitted_date)
        else:
            if len(l_submission.comments) > 0:
                l_submission.submitted_date = l_submission.comments[0].date
                l_submission.submitted_day = date_to_day(a_start.start_date, l_submission.submitted_date)
            else:
                l_submission.submitted_date = a_assignment.assignment_date
                l_submission.submitted_day = date_to_day(a_start.start_date, l_submission.submitted_date)
        return l_submission


def add_missed_assignments(start, course, results, perspective):
    if perspective.name == start.attendance_perspective:
        return
    if len(perspective.assignment_groups) == 1:
        l_assignment_group = course.find_assignment_group(perspective.assignment_groups[0])
        if l_assignment_group is None:
            print("S06 Assignment_group for perspective not found in course", perspective.assignment_groups[0])
            return
        l_assignments = l_assignment_group.assignments[:]
        # remove already submitted
        for l_submission in perspective.submissions:
            l_assignments = remove_assignment(l_assignments, l_submission)
        # open assignments
        for l_assignment in l_assignments:
            if date_to_day(start.start_date, l_assignment.assignment_date) < results.actual_day:
                l_submission = Submission(0, l_assignment.group_id, l_assignment.id, 0, l_assignment.name,
                                          l_assignment.assignment_date,
                                          date_to_day(start.start_date, l_assignment.assignment_date),
                                          l_assignment.assignment_date,
                                          date_to_day(start.start_date, l_assignment.assignment_date),
                                          True, "Systeem", l_assignment.assignment_date, 0, l_assignment.points, 0)
                l_submission.comments.append(Comment(0, "Systeem", l_assignment.assignment_date, NO_SUBMISSION))
                perspective.submissions.append(l_submission)
    elif len(perspective.assignment_groups) > 1:
        print("S07 Perspective has more then one assignment_groups attached", perspective.name,
              perspective.assignment_groups)
    else:
        print("S08 Perspective has no assignment_groups attached", perspective.name, perspective.assignment_groups)


def read_submissions(a_canvas_course, a_start, a_course, a_results, a_total_refresh):
    for assignment_group in a_course.assignment_groups:
        for assignment in assignment_group.assignments:
            print("Processing Assignment {0:6} - {1} {2}".format(assignment.id, assignment_group.name, assignment.name))
            if not a_total_refresh and ((a_results.actual_date - assignment.assignment_date).days > 10):
                # deadline langer dan twee weken geleden. Alle feedback is gegeven.
                continue
            if assignment.unlock_date:
                if assignment.unlock_date > a_results.actual_date:
                    # volgende assignment
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
                                if l_perspective == "peil":
                                    student.student_progress.put_submission(l_submission)
                                else:
                                    this_perspective = student.perspectives[l_perspective.name]
                                    if this_perspective:
                                        if a_total_refresh:
                                            this_perspective.submissions.append(l_submission)
                                        else:
                                            this_perspective.put_submission(l_submission)

                            else:
                                print(f"R21 clould not find perspective for assignment_group {assignment_group.name}")
                        # else:
                        #     print(f"R22 Error creating submission {assignment.name} for student {student.name}")
                    # else:
                    #     print("R23 Could not find student", canvas_submission.user_id)
            else:
                print("R25 Could not find assignment", canvas_assignment.id, "within group", assignment_group.id)

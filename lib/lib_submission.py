from lib.lib_date import get_date_time_obj, date_to_day
from model.Comment import Comment
from model.Submission import Submission

NOT_GRADED = "Nog niet beoordeeld."
NO_SUBMISSION = "Niets ingeleverd voor de deadline"
NO_DATA = "Geen data"


def get_sum_score(a_perspective, a_start_date):
    l_sum_score = 0
    l_last_score = 0
    for submission in a_perspective.submissions:
        if submission.graded:
            l_sum_score += submission.score
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


def submission_builder(a_student, a_assignment, a_canvas_submission, a_assignment_date):
    if a_canvas_submission.score:
        if a_canvas_submission.grade.isnumeric():
            score = float(a_canvas_submission.grade)
        elif a_canvas_submission.grade == 'complete':
            score = 1.0
        elif a_canvas_submission.grade == 'incomplete':
            score = 0.5
        else:
            score = round(a_canvas_submission.score, 2)
        graded = True
    else:
        score = 0
        if a_canvas_submission.grader_id:
            graded = True
        else:
            graded = False
    # maak een submission en voeg de commentaren toe
    canvas_comments = a_canvas_submission.submission_comments
    if not a_canvas_submission.submitted_at and len(canvas_comments) == 0 and not graded:
        return None
    else:
        l_submission = Submission(a_canvas_submission.id, a_assignment.group_id, a_assignment.id, a_student.id,
                                  a_assignment.name, a_assignment_date, None, graded, score,
                                  a_assignment.points)
        for canvas_comment in canvas_comments:
            l_submission.comments.append(
                    Comment(canvas_comment['author_id'], canvas_comment['author_name'],
                    get_date_time_obj(canvas_comment['created_at']), canvas_comment['comment']))
        #bepaal de date/time van het datapunt
        if a_canvas_submission.submitted_at:
            l_submission.submitted_date = get_date_time_obj(a_canvas_submission.submitted_at)
        else:
            if len(l_submission.comments) > 0:
                l_submission.submitted_date = l_submission.comments[0].date
            else:
                l_submission.submitted_date = a_assignment_date
        return l_submission

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
            print(submission.assignment_name, submission.score, l_sum_score)
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


def get_rubric_score(rubrics_assessment):
    submission_score = 0.00
    criterium_scores = []
    if rubrics_assessment:
        # try:
            for canvas_criterium in rubrics_assessment:
                # print(canvas_criterium)
                id = canvas_criterium[0]
                try:
                    points = canvas_criterium[1]['points']
                    submission_score += points
                except:
                    print(
                        f"R41 Fout in criterium_score criterium {canvas_criterium} canvas_submission {rubrics_assessment}")
                criterium_score = CriteriumScore(id, canvas_criterium[1]['rating_id'], points,
                                                 canvas_criterium[1]['comments'])
                criterium_scores.append(criterium_score)
        # except:
        #     print(f"R42 Fout in bepalen rubric_score {rubrics_assessment}")
    return criterium_scores, round(submission_score, 2)


def submission_builder(a_start, a_course, a_student, a_assignment, a_canvas_submission):
    if a_canvas_submission.grade:
        graded = True
    else:
        # print("--", a_assignment.name, a_assignment.points, a_canvas_submission.grade, "score = 0")
        score = 0
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
        if a_assignment.grading_type == "letter_grade":
            rubrics_scores, score = get_rubric_score(rubrics_assessment)
        elif a_assignment.grading_type == "pass_fail":
            if a_canvas_submission.grade == 'complete':
                score = 1.0
            elif a_canvas_submission.grade == 'incomplete':
                score = 0.0
        elif a_assignment.grading_type == "points":
            if graded:
                submission_score = round(a_canvas_submission.score, 2)
                rubrics_scores, rubric_score = get_rubric_score(rubrics_assessment)
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
            print(f"Unknown grading_type {a_assignment.grading_type} for assignment {a_assignment.name}")

        l_submission = Submission(a_canvas_submission.id, a_assignment.group_id, a_assignment.id, a_student.id,
                                  a_assignment.name, a_assignment.assignment_date, None, None, graded, a_canvas_submission.grader_id, score,
                                  a_assignment.points, 0)
        l_submission.rubrics = rubrics_scores
        for canvas_comment in canvas_comments:
            l_submission.comments.append(
                Comment(canvas_comment['author_id'], canvas_comment['author_name'],
                        get_date_time_obj(canvas_comment['created_at']), canvas_comment['comment']))
        # for criterium in a_canvas_submission.rubric_assessment.items():
        #     print("criterium:", criterium)
            # print("Geen rubrics score voor", a_assignment.name)
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


def get_progress(start, course, results, perspective):
    # bepaal de voortgang
    if len(perspective.assignment_groups) == 1:
        assignment_group = course.find_assignment_group(perspective.assignment_groups[0])
        if assignment_group is not None:
            if perspective.name == start.attendance_perspective:
                perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_date)
                total_score = 0
                total_count = 0
                for submission in perspective.submissions:
                    perspective.last_score = date_to_day(start.start_date, submission.submitted_date)
                    total_score += submission.score
                    total_count += 1
                    submission.flow = total_score / total_count * 100 / 2
                    # print(submission.flow)
                    perspective.sum_score = total_score
                perspective.progress = assignment_group.bandwidth.get_progress(assignment_group.strategy,
                                                                               results.actual_day,
                                                                               perspective.last_score,
                                                                               total_score / total_count * 100 / 2)
            elif assignment_group.bandwidth is not None:
                if len(perspective.submissions) > 0:
                    perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_date)
                    total_score = 0
                    total_count = 0
                    for submission in perspective.submissions:
                        if submission.graded:
                            perspective.last_score = date_to_day(start.start_date, submission.submitted_date)
                            total_score += submission.score
                            total_count += 1
                            submission.flow = assignment_group.bandwidth.get_progress_range(perspective.last_score, total_score)
                            # print(submission.flow)
                            perspective.sum_score = total_score
                            # print("Graded")
                        else:
                            pass
                            # print("Not graded")
                    if total_count == 0:
                        # Niet te bepalen
                        perspective.progress = -1
                    elif perspective.last_score != 0:
                        perspective.progress = assignment_group.bandwidth.get_progress(assignment_group.strategy,
                                                                                       results.actual_day,
                                                                                       perspective.last_score,
                                                                                       perspective.sum_score)
                    else:
                        # Niet te bepalen
                        perspective.progress = -1
                else:
                    # Niet te bepalen
                    perspective.progress = -1
            else:
                # Niet te bepalen
                perspective.progress = -1
        else:
            print("Could not find assignment_group with id", perspective.assignment_groups[0])
    elif len(perspective.assignment_groups) > 1:
        print("Perspective has more then one assignment_groups attached", perspective.name,
              perspective.assignment_groups)
    else:
        print("Perspective has no assignment_groups attached", perspective.name, perspective.assignment_groups)


def add_missed_assignments(start, course, results, perspective):
    if perspective.name == start.attendance_perspective:
        return
    if len(perspective.assignment_groups) == 1:
        l_assignment_group = course.find_assignment_group(perspective.assignment_groups[0])
        if l_assignment_group is None:
            return
        l_assignments = l_assignment_group.assignments[:]
        # remove already submitted
        for l_submission in perspective.submissions:
            l_assignments = remove_assignment(l_assignments, l_submission)
        # open assignments
        for l_assignment in l_assignments:
            if date_to_day(start.start_date, l_assignment.assignment_date) < results.actual_day:
                l_submission = Submission(0, l_assignment.group_id, l_assignment.id, 0, l_assignment.name,
                                          l_assignment.assignment_date, l_assignment.assignment_date,
                                          date_to_day(start.start_date, l_assignment.assignment_date),
                                          True, 0, 0, l_assignment.points, 0)
                l_submission.comments.append(Comment(0, "Systeem", l_assignment.assignment_date, NO_SUBMISSION))
                perspective.submissions.append(l_submission)
    elif len(perspective.assignment_groups) > 1:
        print("Perspective has more then one assignment_groups attached", perspective.name,
              perspective.assignment_groups)
    else:
        print("Perspective has no assignment_groups attached", perspective.name, perspective.assignment_groups)

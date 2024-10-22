import textwrap
from lib.lib_date import get_date_time_loc
from lib.lib_submission import NO_DATA
from model.perspective.Status import NOT_YET_GRADED, BEFORE_DEADLINE


def get_punten_str(points):
    if points == 1:
        return " punt"
    else:
        return " punten"


def get_hover_assignment(points, data_point):
    if "AssignmentSequence" in str(type(data_point)):
        # geen oplevering
        assignment_sequence = data_point
        if points:
            return "<b>" + assignment_sequence.name + "</b><br>Deadline " + get_date_time_loc(assignment_sequence.assignments[0].assignment_date) + ", " + str(assignment_sequence.points) + get_punten_str(assignment_sequence.points)
        else:
            return "<b>" + assignment_sequence.name + "</b><br>Deadline " + get_date_time_loc(assignment_sequence.assignments[0].assignment_date)
    elif "Assignment" in str(type(data_point)):
        assignment = data_point
        if points:
            return "<b>" + assignment.name + "</b><br>Deadline " + get_date_time_loc(assignment.assignment_date) + ", " + str(assignment.points) + get_punten_str(assignment.points)
        else:
            return "<b>" + assignment.name + "</b><br>Deadline " + get_date_time_loc(assignment.assignment_date)
    else:
        submission = data_point
        if points:
            return "<b>" + submission.assignment_name + "</b><br>Deadline " + get_date_time_loc(submission.assignment_date) + ", " + str(submission.points) + get_punten_str(submission.points)
        else:
            return "<b>" + submission.assignment_name + "</b><br>Deadline " + get_date_time_loc(submission.assignment_date)


def get_hover_grade(course, submission, grades, level):
    l_hover = "<br>Ingeleverd " + get_date_time_loc(submission.submitted_date)
    l_label = grades[str(level)].label
    l_hover += "<br><b>" + l_label + "</b>, beoordeeld door " + str(submission.grader_name) + " op " + get_date_time_loc(submission.graded_date)
    if course.find_perspective_by_assignment_group(submission.assignment_group_id).show_points:
        l_hover += ", score: " + str(submission.score)
    l_hover += "<br>"
    return l_hover


def get_hover_status(submission, level_serie):
    l_hover = "<br>Ingeleverd " + get_date_time_loc(submission.submitted_date)
    l_hover += "<br><b>" + level_serie.get_status(submission.status).label + "</b>"
    l_hover += "<br>"
    return l_hover


def get_hover_attendance(attendance, attendance_submission, grades, level):
    l_hover = "<br><b>Aanwezigheid</b> op " + get_date_time_loc(attendance_submission.date)
    l_label = grades[str(level)].label
    l_hover += "<br><b>" + l_label + "</b>, opgemaakt door " + str(attendance_submission.teacher)
    if attendance.show_points:
        l_hover += ", score: " + str(attendance_submission.score)
    return l_hover


def get_hover_peiling(a_peil_submissions, a_course, a_level_serie_collections):
    hover = NO_DATA
    if a_peil_submissions:
        hover = "<b>" + a_peil_submissions.assignment_name + "</b> " + get_date_time_loc(a_peil_submissions.assignment_date) + "<br>"
        if a_peil_submissions.graded:
            if "beoordeling".lower() in a_peil_submissions.assignment_name.lower():
                hover += a_level_serie_collections.level_series[a_course.grade_levels].grades[str(int(a_peil_submissions.score))].label
            else:
                hover += a_level_serie_collections.level_series[a_course.level_moments.levels].grades[str(int(a_peil_submissions.score))].label
            hover += ", bepaald door " + str(a_peil_submissions.grader_name) + " op " + get_date_time_loc(a_peil_submissions.graded_date)
            hover += get_hover_comments(a_peil_submissions.comments)
            hover += get_hover_rubrics_comments(a_course, a_peil_submissions, a_level_serie_collections.level_series[a_course.grade_levels].grades)
        else:
            if "beoordeling".lower() in a_peil_submissions.assignment_name.lower():
                hover += a_level_serie_collections.level_series[a_course.grade_levels].get_status(BEFORE_DEADLINE).label
            else:
                hover += a_level_serie_collections.level_series[a_course.level_moments.levels].get_status(BEFORE_DEADLINE).label
    return hover


def get_hover_comments(comments):
    l_hover = ""
    if len(comments) > 0:
        l_hover += "<br><b>Commentaar/Feedback:</b>"
        line_nr = 0
        for comment in comments:
            value = comment.author_name + " - <i>" + comment.comment + "</i>"
            wrapper = textwrap.TextWrapper(width=125)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                if line_nr > 5:
                    l_hover += "<br>Te veel commentaar/feedback zie Canvas."
                    return l_hover
                l_hover += "<br>" + line
                line_nr += 1
    return l_hover


def get_hover_rubrics_comments(course, submission, grades):
    if len(submission.rubrics) == 0:
        return ""
    l_hover = "<br><b>Criteria:</b>"
    for criterion_score in submission.rubrics:
        # print("BP10 -", submission.assignment_id, criterion_score)
        assignment = course.find_assignment(submission.assignment_id)
        # print("BP11 -", assignment)
        assignment_criterion = assignment.get_criterion(criterion_score.id)
        if assignment_criterion is None:
            continue
        # if submission.assignment_id ==  298261 and submission.student_id == 148369:
        # print("BP11 -", assignment_criterion, criterion_score)
        if criterion_score.rating_id:
            if assignment_criterion.get_rating(criterion_score.rating_id) is not None:
                l_hover += "<br>- " + assignment_criterion.description + " <b>" + assignment_criterion.get_rating(criterion_score.rating_id).description + "</b>"
            # if submission.assignment_id == 298261 and submission.student_id == 148369:
            #     print("BP14 -", l_hover)
        else:
            if criterion_score.score == 0:
                l_hover += "<br>- " + assignment_criterion.description + " <b>"+grades[str(int(criterion_score.score))].label+"</b>"
                # if submission.assignment_id == 298261 and submission.student_id == 148369:
                #     print("BP15 -", l_hover)
            else:
                l_hover += "<br>- " + assignment_criterion.description + " <b>"+str(criterion_score.score)+"</b>"
                # if submission.assignment_id == 298261 and submission.student_id == 148369:
                #     print("BP16 -", l_hover)

        if criterion_score.comment:
            value = "<i>" + criterion_score.comment + "</i>"
            wrapper = textwrap.TextWrapper(width=125)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                l_hover += "<br>" + line
        # if submission.assignment_id == 298261 and submission.student_id == 148369:
        #     print("BP20 -", l_hover)
    return l_hover


def get_hover_day_bar(l_label, a_actual_day, a_actual_date, a_show_points, a_score):
    l_hover = f"<b>{l_label}</b>"
    l_hover += f"<br>dag {a_actual_day} in onderwijsperiode [{a_actual_date}]"
    if a_show_points:
        l_hover += f"<br>{int(a_score)} {get_punten_str(int(a_score))}"
    return l_hover


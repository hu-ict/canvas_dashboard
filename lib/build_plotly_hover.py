import textwrap
from lib.lib_date import date_to_day, get_date_time_loc
from lib.lib_submission import NOT_GRADED, NO_DATA


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
            return "<b>" + assignment_sequence.name + "</b>, " + str(assignment_sequence.points) + get_punten_str(assignment_sequence.points) + ", deadline " + get_date_time_loc(assignment_sequence.assignments[0].assignment_date)
        else:
            return "<b>" + assignment_sequence.name + "</b>, deadline " + get_date_time_loc(assignment_sequence.assignments[0].assignment_date)
    elif "Assignment" in str(type(data_point)):
        assignment = data_point
        if points:
            return "<b>" + assignment.name + "</b>, " + str(assignment.points) + get_punten_str(assignment.points) + ", deadline " + get_date_time_loc(assignment.assignment_date)
        else:
            return "<b>" + assignment.name + "</b>, deadline " + get_date_time_loc(assignment.assignment_date)
    else:
        submission = data_point
        if points:
            return "<b>" + submission.assignment_name + "</b>, " + str(submission.points) + get_punten_str(submission.points) + ", deadline " + get_date_time_loc(submission.submitted_date)
        else:
            return "<b>" + submission.assignment_name + "</b>, deadline " + get_date_time_loc(submission.assignment_date)


def get_hover_grade(a_labels_colors, a_course, a_perspective, level, submission):
    l_hover = "<br>Ingeleverd " + get_date_time_loc(submission.submitted_date)
    if submission.graded:
        l_label = a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].label
        l_hover += "<br><b>" + l_label + "</b>, beoordeeld door " + str(submission.grader_name) + " op " + get_date_time_loc(submission.graded_date)
        if a_course.find_perspective_by_assignment_group(submission.assignment_group_id).show_points:
            l_hover += ", score: " + str(submission.score)
    else:
        l_hover += "<br><b>" + NOT_GRADED + "</b>"
    return l_hover


def get_hover_attendance(a_attendance, a_attendance_submission, a_level, a_levels):
    l_hover = "<br><b>Aanwezigheid</b> op " + get_date_time_loc(a_attendance_submission.date)
    if a_attendance_submission.graded:
        l_label = a_levels.level_series[a_attendance.levels].levels[str(a_level)].label
        l_hover += "<br><b>" + l_label + "</b>, opgemaakt door " + str(a_attendance_submission.teacher)
        if a_attendance.show_points:
            l_hover += ", score: " + str(a_attendance_submission.score)
    else:
        l_hover += "<br><b>Niet bepaald</b>"
    return l_hover


def get_hover_peiling(a_peil_submissions, a_start, a_course, a_levels):
    hover = NO_DATA
    if a_peil_submissions:
        if a_peil_submissions.graded:
            score = a_peil_submissions.score
        else:
            score = -1
        hover = "<b>" + a_peil_submissions.assignment_name + "</b> " + get_date_time_loc(a_peil_submissions.assignment_date) + "<br>"
        if "beoordeling".lower() in a_peil_submissions.assignment_name.lower():
            hover += a_levels.level_series[a_start.grade_levels].levels[str(int(score))].label
        else:
            hover += a_levels.level_series[a_start.level_moments.levels].levels[str(int(score))].label
        if score > -1:
            hover += ", bepaald door " + str(a_peil_submissions.grader_name) + " op " + get_date_time_loc(a_peil_submissions.graded_date)
            hover += get_hover_comments(a_peil_submissions.comments)
            hover += get_hover_rubrics_comments(a_course, a_peil_submissions, a_levels)
    return hover


def get_hover_comments(comments):
    l_hover = ""
    if len(comments) > 0:
        l_hover += "<br><b>Commentaar:</b>"
        for comment in comments:
            value = comment.author_name + " - <i>" + comment.comment + "</i>"
            wrapper = textwrap.TextWrapper(width=125)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                l_hover += "<br>" + line
    return l_hover


def get_hover_rubrics_comments(course, submission, levels):
    if len(submission.rubrics) == 0:
        return ""
    l_hover = "<br><b>Criteria:</b>"
    for criterion_score in submission.rubrics:
        # print("BP10 -", submission.assignment_id, criterion_score)
        assignment = course.find_assignment(submission.assignment_id)
        # print("BP11 -", assignment)
        assignment_criterion = assignment.get_criterion(criterion_score.id)
        # if submission.assignment_id ==  298261 and submission.student_id == 148369:
        # print("BP11 -", assignment_criterion, criterion_score)
        if criterion_score.rating_id:
            l_hover += "<br>- " + assignment_criterion.description + " <b>" + assignment_criterion.get_rating(criterion_score.rating_id).description + "</b>"
            # if submission.assignment_id == 298261 and submission.student_id == 148369:
            #     print("BP14 -", l_hover)
        else:
            if criterion_score.score == 0:
                l_hover += "<br>- " + assignment_criterion.description + " <b>"+levels.level_series["niveau"].levels[str(int(criterion_score.score))].label+"</b>"
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


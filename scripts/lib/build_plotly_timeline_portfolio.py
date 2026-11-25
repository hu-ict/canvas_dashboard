from scripts.lib.build_hover import get_hover_assignment, get_hover_status, get_hover_comments, get_hover_grade, \
    get_rubrics_comments, get_hover_moment, get_hover_feedback
from scripts.lib.build_plotly_perspective import get_moments, plot_day_bar_lu
from scripts.lib.lib_date import get_date_time_loc
from scripts.lib.lib_plotly import get_marker_size, hover_style
from scripts.model.perspective.Status import VIEW_UNPOSTED, BEFORE_DEADLINE
import plotly.graph_objs as go

def plot_timeline_portfolio(a_row, a_col, a_fig, a_course, a_student, a_level_serie_collection):
    # l_perspective = a_course.perspectives[a_student_perspective.name]
    y_colors = [a_level_serie_collection.level_series[a_course.level_moments.levels].get_status(BEFORE_DEADLINE).color]
    x_portfolio = [0]
    y_portfolio = ["P<br>Portfolio"]
    y_hover = ['<b>Start</b> ' + get_date_time_loc(a_course.start_date)]
    y_size = [get_marker_size(False)]
    y_marker_symbols = ["circle"]

    for student_perspective in a_student.perspectives.values():
        for submission_sequence in student_perspective.submission_sequences:
            assignment_group_levels = a_course.get_assignment_group(submission_sequence.get_assignment_group_id()).levels
            # print("BPP51 -", submission_sequence.get_assignment.group_id(), submission_sequence.tag, assignment_group_levels)
            l_level_serie = a_level_serie_collection.level_series[assignment_group_levels]
            y_size.append(get_marker_size(submission_sequence.is_graded()))
            x_portfolio.append(submission_sequence.get_day())

            if submission_sequence.is_graded() and (submission_sequence.is_posted() or VIEW_UNPOSTED):
                grade = l_level_serie.grades[submission_sequence.get_grade()]
                y_colors.append(grade.color)
            else:
                color = a_level_serie_collection.level_series[assignment_group_levels].get_status(BEFORE_DEADLINE).color
                y_colors.append(color)
            y_marker_symbols.append(a_course.get_assignment_group_by_assignment_sequence_tag(submission_sequence.tag).marker)
            submission_nr = 0
            l_hover = ""
            for submission in submission_sequence.submissions:
                l_hover += get_hover_assignment(True, submission)
                if submission.graded and (submission.posted or VIEW_UNPOSTED):
                    grade = l_level_serie.grades[submission.grade]
                    l_hover += get_hover_grade(a_course, submission, grade)
                else:
                    status = l_level_serie.status[submission.status]
                    l_hover += get_hover_status(submission, status)
                if submission.posted or VIEW_UNPOSTED:
                    l_hover += get_hover_comments(submission.comments)
                    if submission.graded:
                        grade = l_level_serie.grades[submission.grade]
                        l_hover += get_rubrics_comments(a_course, submission, grade, True)
                if submission_nr < len(submission_sequence.submissions) - 1:
                    l_hover += "<br><br>"
            if len(l_hover) > 4000:
                l_hover = l_hover[
                          :4000] + "<br>Te veel commentaar/feedback voor pop-up. Ga naar Canvas voor de complete tekst."
            y_hover.append(l_hover)
            y_portfolio.append("P<br>Portfolio")
    a_fig.add_trace(
        go.Scatter(
            x=x_portfolio,
            y=y_portfolio,
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines+markers',
            marker_color=y_colors,
            marker_symbol=y_marker_symbols,
            line_color="#444444",
            hoverlabel=hover_style,
            marker=dict(
                size=y_size,
                opacity=1.0,
                line=dict(
                    width=2
                )
            )
        ),
        row=a_row, col=a_col
    )


def plot_timeline_moments(a_row, a_col, a_fig, a_course, a_submission_list, a_level_serie_collection):
    x_feedback = [0]
    y_feedback = ["BP<br>Peil/Beslissing"]
    y_hover = ['<b>Start</b> ' + get_date_time_loc(a_course.start_date)]
    y_colors = [a_level_serie_collection.level_series[a_course.level_moments.levels].get_status(BEFORE_DEADLINE).color]
    y_size = [get_marker_size(False)]
    y_marker_symbols = ["circle"]
    for submission in a_submission_list:
        levels = a_course.get_assignment_group(submission.assignment.group_id).levels
        level_serie = a_level_serie_collection.level_series[levels]
        y_size.append(get_marker_size(True))
        x_feedback.append(submission.assignment.day)
        y_feedback.append("BP<br>Peil/Beslissing")
        # print("BPP61 -", submission.assignment.name, submission.graded, submission.grade)
        y_hover.append(get_hover_moment(a_course, submission, level_serie))
        if submission.graded and (submission.posted or VIEW_UNPOSTED):
            y_colors.append(level_serie.grades[submission.grade].color)
        else:
            y_colors.append(level_serie.get_status(BEFORE_DEADLINE).color)
        y_marker_symbols.append(a_course.get_assignment_group_by_assignment(submission.assignment.id).marker)
    a_fig.add_trace(
        go.Scatter(
            x=x_feedback,
            y=y_feedback,
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines+markers',
            marker_color=y_colors,
            marker_symbol=y_marker_symbols,
            line_color="#444444",
            hoverlabel=hover_style,
            marker=dict(
                size=y_size,
                opacity=1.0,
                line=dict(
                    width=2
                )
            )
        ),
        row=a_row, col=a_col
    )


def plot_timeline_gf(a_row, a_col, a_fig, a_course, a_feedback_list, a_feedback_colors):
    x_feedback = [0]
    y_feedback = ["AF<br>Algemene feedback"]
    y_hover = ['<b>Start</b> ' + get_date_time_loc(a_course.start_date)]
    y_colors = [a_feedback_colors["N"]["color"]]
    y_size = [get_marker_size(False)]
    y_marker_symbols = ["circle"]
    for feedback in a_feedback_list:
        y_size.append(get_marker_size(True))
        x_feedback.append(feedback.day)
        y_feedback.append("AF<br>Algemene feedback")
        y_hover.append(get_hover_feedback("Dialoog", feedback))
        y_colors.append(a_feedback_colors["N"]["color"])
        assigment_group = a_course.get_assignment_group_by_assignment(feedback.assignment_id)
        marker_symbol = assigment_group.marker
        y_marker_symbols.append(marker_symbol)
    a_fig.add_trace(
        go.Scatter(
            x=x_feedback,
            y=y_feedback,
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines+markers',
            marker_color=y_colors,
            marker_symbol=y_marker_symbols,
            line_color="#444444",
            hoverlabel=hover_style,
            marker=dict(
                size=y_size,
                opacity=1.0,
                line=dict(
                    width=2
                )
            )
        ),
        row=a_row, col=a_col
    )


def plot_timeline_lu(a_row, a_col, a_fig, a_course, a_learning_outcome, a_feedback_colors, a_level_serie_collection):

    x_feedback = [0]
    y_feedback = [a_learning_outcome.id + "<br>" + a_learning_outcome.short]
    y_hover = ['<b>Start</b> ' + get_date_time_loc(a_course.start_date)]
    if VIEW_UNPOSTED:
        y_hover[0] += "<br>Saturatie op LU "
        y_colors = [a_level_serie_collection.level_series[a_course.level_moments.levels].get_grades(a_learning_outcome.saturation).color]
    else:
        y_colors = [a_feedback_colors["N"]["color"]]
    y_size = [get_marker_size(False)]
    y_marker_symbols = ["circle"]
    for feedback in a_learning_outcome.feedback_list:
        y_size.append(get_marker_size(True))
        x_feedback.append(feedback.day)
        y_feedback.append(a_learning_outcome.id + "<br>" + a_learning_outcome.short)
        y_hover.append(get_hover_feedback("Observatie", feedback))
        y_colors.append(a_feedback_colors[feedback.positive_neutral_negative]["color"])
        y_marker_symbols.append(a_course.get_assignment_group_by_assignment(feedback.assignment_id).marker)
    a_fig.add_trace(
        go.Scatter(
            x=x_feedback,
            y=y_feedback,
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines+markers',
            marker_color=y_colors,
            marker_symbol=y_marker_symbols,
            line_color="#444444",
            hoverlabel=hover_style,
            marker=dict(
                size=y_size,
                opacity=1.0,
                line=dict(
                    width=2
                )
            )
        ),
        row=a_row, col=a_col
    )
    a_fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester], row=a_row,
                       col=a_col)

def plot_timeline(a_row, a_col, a_fig, a_course, a_student, a_actual_day, a_actual_date, a_level_serie_collection,
                  a_feedback_colors):
    a_fig.update_yaxes(title_text="Leeruitkomsten",
                       # range=[0, len(a_student.learning_outcomes)+1],
                       row=a_row, col=a_col)

    assignment_group = a_course.get_assignment_group(a_course.level_moments.assignment_group_ids[0])
    moments = get_moments(a_course, assignment_group, a_student)
    assignment_group = a_course.get_assignment_group(a_course.grade_moments.assignment_group_ids[0])
    moments.extend(get_moments(a_course, assignment_group, a_student))
    plot_timeline_moments(a_row, a_col, a_fig, a_course, moments, a_level_serie_collection)
    plot_timeline_gf(a_row, a_col, a_fig, a_course, a_student.general_feedback_list, a_feedback_colors)
    learning_outcomes_list = list(a_student.learning_outcomes.values())
    learning_outcomes_list = sorted(learning_outcomes_list, key=lambda x: x.id.lower(), reverse=True)
    for learning_outcome in learning_outcomes_list:
        # print("BPP11 -", timeline_lu)
        plot_timeline_lu(a_row, a_col, a_fig, a_course, learning_outcome, a_feedback_colors, a_level_serie_collection)


    # print("BPP71 - Moments", moments)
    plot_timeline_portfolio(a_row, a_col, a_fig, a_course, a_student, a_level_serie_collection)

    plot_day_bar_lu(a_row, a_col, a_fig, a_actual_day, a_actual_date,
                    a_student.progress, a_level_serie_collection.level_series["progress"].grades,
                    learning_outcomes_list[0].id + "<br>" + learning_outcomes_list[0].short)
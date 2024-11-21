import plotly.graph_objs as go

from lib.build_plotly_hover import get_hover_attendance
from lib.build_plotly_perspective import plot_bandbreedte_colored, plot_day_bar
from lib.lib_date import date_to_day, get_date_time_loc
from lib.lib_plotly import get_marker_size, hover_style
from model.perspective.Status import BEFORE_DEADLINE


def plot_attendance_submissions(a_row, a_col, a_fig, a_course, a_attendance_submissions,
                                a_level_serie):
    x_submission = [0]
    if a_course.attendance.show_flow:
        y_submission = [0.5]
    else:
        y_submission = [100]
    y_hover = ['<b>Start</b> ' + get_date_time_loc(a_course.start_date)]
    y_colors = [a_level_serie.get_status(BEFORE_DEADLINE).color]
    y_size = [get_marker_size(False)]
    # cum_score = 0
    for attendance_submission in a_attendance_submissions:

        y_size.append(get_marker_size(True))
        x_submission.append(attendance_submission.day)

        # cum_score += attendance_submission.flow
        grade = a_level_serie.grades[attendance_submission.grade]
        y_colors.append(grade.color)
        l_hover = get_hover_attendance(a_course.attendance, attendance_submission, grade)

        y_hover.append(l_hover)
        if a_course.attendance.show_flow:
            y_submission.append(round(attendance_submission.flow * 100, 0))
        else:
            y_submission.append(round(attendance_submission.flow * 100, 0))

    a_fig.add_trace(
        go.Scatter(
            x=x_submission,
            y=y_submission,
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines+markers',
            marker_color=y_colors,
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
    return {"x": x_submission, "y": y_submission}


def plot_attendance_perspective(a_row, a_col, a_fig, a_course, a_attendance_perspective,
                    a_actual_day, a_actual_date, a_level_serie_collection):
    # print("BP66", a_attendance_perspective)
    # print("BP67", a_attendance_perspective.attendance_submissions)
    plot_bandbreedte_colored(a_row, a_col, a_fig,
                             a_course.days_in_semester, a_course.attendance.bandwidth, a_course.attendance.show_flow,
                             a_course.attendance.total_points)
    plot_day_bar(a_row, a_col, a_fig,
                 a_course,
                 a_course.attendance.total_points, a_actual_day, a_actual_date, a_attendance_perspective.progress,
                 a_level_serie_collection.level_series[a_course.level_moments.levels].grades, a_course.attendance.show_points, a_course.attendance.show_flow,
                 a_attendance_perspective.essential_percentage)
    plot_attendance_submissions(a_row, a_col, a_fig,
                                a_course, a_attendance_perspective.attendance_submissions,
                                a_level_serie_collection.level_series[a_course.attendance.levels])
    # plot_open_assignments(a_row, a_col, a_fig, a_start, a_course, show_points, l_assignments, a_levels)
    a_fig.update_yaxes(title_text="Percentage aanwezig", range=[0, a_course.attendance.total_points], row=a_row,
                       col=a_col)
    a_fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester], row=a_row,
                       col=a_col)

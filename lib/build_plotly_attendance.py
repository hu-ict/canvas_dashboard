import plotly.graph_objs as go

from lib.build_plotly_hover import get_hover_attendance
from lib.build_plotly_perspective import plot_bandbreedte_colored
from lib.lib_date import date_to_day, get_date_time_loc
from lib.lib_plotly import get_marker_size, hover_style


def plot_attendance_submissions(a_row, a_col, a_fig, a_start, a_course, a_attendance, a_attendance_submissions, a_levels):
    x_submission = [0]
    if a_attendance.show_flow:
        y_submission = [0.5]
    else:
        y_submission = [100]
    y_hover = ['<b>Start</b> '+get_date_time_loc(a_start.start_date)]
    y_colors = [a_levels.level_series[a_start.progress_levels].levels["-1"].color]
    y_size = [get_marker_size(False)]
    cum_score = 0
    for attendance_submission in a_attendance_submissions:
        y_size.append(get_marker_size(attendance_submission.graded))
        x_submission.append(attendance_submission.day)

        if attendance_submission.graded:
            cum_score += attendance_submission.flow
            level = a_levels.level_series[a_attendance.levels].get_level_by_fraction(attendance_submission.score / attendance_submission.points)
            y_colors.append(a_levels.level_series[a_attendance.levels].levels[str(level)].color)
            l_hover = get_hover_attendance(a_attendance, attendance_submission, level, a_levels)
        else:
            y_colors.append(a_levels.level_series[a_attendance.levels].levels["-2"].color)
            l_hover = get_hover_attendance(a_attendance, attendance_submission, "", a_levels)
        y_hover.append(l_hover)
        if a_attendance.show_flow:
            y_submission.append(attendance_submission.flow*100)
        else:
            y_submission.append(attendance_submission.flow*100)

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

def plot_attendance(a_row, a_col, a_fig, a_instances, a_start, a_course, a_attendance, a_attendance_perspective,
                     a_actual_day, a_actual_date, a_levels):
    # print("BP66", a_attendance_perspective)
    # print("BP67", a_attendance_perspective.attendance_submissions)

    plot_bandbreedte_colored(a_row, a_col, a_fig, a_course.days_in_semester, a_attendance.bandwidth, a_attendance.show_flow, a_attendance.total_points)
    # plot_day_bar(a_row, a_col, a_fig, a_start, total_points, a_actual_day, a_actual_date, a_attendance_perspective.progress, a_levels, show_points, a_attendance_perspective.sum_score )
    plot_attendance_submissions(a_row, a_col, a_fig, a_start, a_course, a_attendance, a_attendance_perspective.attendance_submissions, a_levels)
    # plot_open_assignments(a_row, a_col, a_fig, a_start, a_course, show_points, l_assignments, a_levels)
    a_fig.update_yaxes(title_text="Percentage aanwezig", range=[0, a_course.attendance.total_points], row=a_row, col=a_col)
    a_fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester], row=a_row, col=a_col)
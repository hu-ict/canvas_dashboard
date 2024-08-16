import copy
import plotly.graph_objs as go

from lib.build_plotly_generic import plot_bandbreedte_colored
from lib.build_plotly_hover import get_hover_peiling, get_hover_assignment, get_hover_day_bar, get_hover_grade, \
    get_hover_comments, get_hover_rubrics_comments
from lib.lib_bandwidth import calc_dev
from lib.lib_date import date_to_day, get_date_time_loc
from lib.lib_plotly import get_marker_size, hover_style


def find_submissions(a_student, a_peil_construction):
    if a_peil_construction is None:
        return
    l_peil_construction = copy.deepcopy(a_peil_construction)
    for l_perspective in l_peil_construction.values():
        for peil in l_perspective:
            l_submission = a_student.get_peilmoment(peil['assignment'].id)
            if l_submission:
                peil['submission'] = l_submission
    return l_peil_construction


def plot_progress(a_row, a_col, a_fig, a_start, a_course, a_perspective, a_levels):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': []}
    for pleiling in a_perspective:
        series['y'].append(0)
        if pleiling['submission']:
            #Heeft beoordeling
            series['size'].append(get_marker_size(True)+2)
            series['hover'].append(get_hover_peiling(pleiling['submission'], a_start, a_course, a_levels))
            series['x'].append(date_to_day(a_start.start_date, pleiling['submission'].submitted_date))
            if "beoordeling" in pleiling['assignment'].name.lower():
                series['color'].append(a_levels.level_series[a_start.grade_levels].levels[str(int(pleiling['submission'].score))].color)
            else:
                series['color'].append(a_levels.level_series[a_start.level_moments.levels].levels[str(int(pleiling['submission'].score))].color)
        else:
            #Heeft nog geen beoordeling
            series['size'].append(get_marker_size(False)+2)
            series['hover'].append("<b>"+pleiling['assignment'].name + "</b> " + get_date_time_loc(pleiling['assignment'].assignment_date))
            series['x'].append(date_to_day(a_start.start_date, pleiling['assignment'].assignment_date))
            if "beoordeling" in pleiling['assignment'].name.lower():
                series['color'].append(a_levels.level_series[a_start.grade_levels].levels["-1"].color)
            else:
                series['color'].append(a_levels.level_series[a_start.level_moments.levels].levels["-1"].color)
    a_fig.add_trace(
        go.Scatter(
            x=series['x'],
            y=series['y'],
            hoverinfo="text",
            hovertext=series['hover'],
            mode='markers',
            marker_color=series['color'],
            hoverlabel=hover_style,
            line_color="#444444",
            marker=dict(
                size=series['size'],
                symbol="arrow-down",
                opacity=1.0,
                line=dict(
                    width=2
                )
            )
        ),
        row=a_row, col=a_col
    )


def plot_assignments(a_row, a_col, a_fig, a_start, a_course, a_show_points, a_assignment_sequences, a_levels):
    series = {"color": [], "size": [], "size2": [], 'x': [], 'x2': [], 'y': [], 'y2': [], 'hover': []}
    cum_points = 0
    y2 = {}
    for day in range(1, a_course.days_in_semester):
        y2[str(day // 7+1)] = 0
    for assignment_sequence in a_assignment_sequences:
        y2[str(assignment_sequence.get_day() // 7+1)] += assignment_sequence.points
    for punt in y2:
        series['x2'].append(int(punt)*7)
        series['y2'].append(y2[punt])
        series['size2'].append(get_marker_size(True))

    y2_max = max(series['y2'])
    for assignment_sequence in a_assignment_sequences:
        series['size'].append(get_marker_size(False))
        series['x'].append(assignment_sequence.get_day())
        cum_points += assignment_sequence.points
        series['y'].append(cum_points)
        series['color'].append(a_levels.level_series[a_start.grade_levels].levels["-1"].color)
        series['hover'].append(get_hover_assignment(a_show_points, assignment_sequence))


    open_assignments = go.Scatter(
        x=series['x'],
        y=series['y'],
        hoverinfo="text",
        hovertext=series['hover'],
        mode='markers',
        marker_color=series['color'],
        line_color="#444444",
        hoverlabel=hover_style,
        marker=dict(
            size=series['size'],
            opacity=1.0,
            line=dict(
                width=2
            )
        )
    )

    workload = go.Scatter(
        x=series['x2'],
        y=series['y2'],
        mode='markers',
        marker_color="#DDDDDD",
        line_color="#333333",
        hoverlabel=hover_style,
        marker=dict(
            size=series['size2'],
            opacity=1.0,
            line=dict(
                width=2
            )
        )
    )

    if a_row == 0:
        a_fig.add_trace(open_assignments, secondary_y=False)
        a_fig.add_trace(workload, secondary_y=True)
        a_fig.update_yaxes(secondary_y=False)
        a_fig.update_yaxes(title_text="Waarde per week", range=[0, y2_max+1], secondary_y=True)
    else:
        a_fig.add_trace(open_assignments, row=a_row, col=a_col)
    return

def plot_future_assignments(a_row, a_col, a_fig, a_start, a_show_points, a_assignment_sequences, a_levels):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': []}
    for assignment_sequence in a_assignment_sequences:
        series['size'].append(get_marker_size(False))
        series['x'].append(assignment_sequence.get_day())
        series['y'].append(0)
        series['color'].append(a_levels.level_series[a_start.grade_levels].levels["-1"].color)
        series['hover'].append(get_hover_assignment(a_show_points, assignment_sequence))
    future_assignments = go.Scatter(
        x=series['x'],
        y=series['y'],
        hoverinfo="text",
        hovertext=series['hover'],
        mode='markers',
        marker_color=series['color'],
        line_color="#444444",
        hoverlabel=hover_style,
        marker=dict(
            size=series['size'],
            opacity=1.0,
            line=dict(
                width=2
            )
        )
    )
    a_fig.add_trace(future_assignments, row=a_row, col=a_col)
    return

def plot_day_bar(a_row, a_col, a_fig, a_start, a_total_points, a_actual_day, a_actual_date, a_progress, a_levels, a_show_points, a_actual_points):
    if a_total_points <= 0:
        return
    l_label = a_levels.level_series[a_start.progress_levels].levels[str(a_progress)].label
    l_color = a_levels.level_series[a_start.progress_levels].levels[str(a_progress)].color
    l_hover = get_hover_day_bar(l_label, a_actual_day, a_actual_date, a_show_points, a_actual_points)

    a_fig.add_trace(
        go.Scatter(
            x=[a_actual_day, a_actual_day+2, a_actual_day+2, a_actual_day, a_actual_day],
            y=[0, 0, a_total_points, a_total_points, 0],
            fill="toself",
            mode='lines',
            name='',
            hoverlabel=hover_style,
            text=l_hover,
            opacity=0
        ),
        row=a_row,
        col=a_col
    )
    a_fig.add_shape(
        dict(type="rect", x0=a_actual_day, x1=a_actual_day+1, y0=0, y1=a_total_points,
             fillcolor=l_color, line_color=l_color
             ),
        row=a_row,
        col=a_col
    )



def plot_submissions(a_row, a_col, a_fig, a_start, a_course, a_perspective, a_levels):
    l_assignment_group = a_course.find_assignment_group(a_perspective.assignment_groups[0])
    l_perspective = a_course.find_perspective_by_name(a_perspective.name)
    x_submission = [0]
    if l_perspective.show_flow:
        y_submission = [0.5]
    else:
        y_submission = [0]
    y_hover = ['<b>Start</b> '+get_date_time_loc(a_start.start_date)]
    y_colors = [a_levels.level_series[a_start.progress_levels].levels["-1"].color]
    y_size = [get_marker_size(False)]
    cum_score = 0
    for submission_sequence in a_perspective.submission_sequences:
        y_size.append(get_marker_size(submission_sequence.is_graded()))
        x_submission.append(submission_sequence.get_day())
        if submission_sequence.is_graded():
            cum_score += submission_sequence.get_score()
            if submission_sequence.points == 0:
                # lelijke hack
                submission_sequence.points = 1
            level = a_levels.level_series[a_course.perspectives[a_perspective.name].levels].get_level_by_fraction(submission_sequence.get_score() / submission_sequence.points)
            y_colors.append(a_levels.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].color)
        else:
            y_colors.append(a_levels.level_series[a_course.perspectives[a_perspective.name].levels].levels["-2"].color)

        l_hover = ""
        for submission in submission_sequence.submissions:
            level = a_levels.level_series[a_course.perspectives[a_perspective.name].levels].get_level_by_fraction(submission.score / submission_sequence.points)
            l_hover += get_hover_assignment(l_perspective.show_points, submission)
            if submission_sequence.is_graded():
                l_hover += get_hover_grade(a_levels, a_course, a_perspective, level, submission)
            else:
                l_hover += get_hover_grade(a_levels, a_course, a_perspective, "", submission)
            l_hover += get_hover_comments(submission.comments)
            l_hover += get_hover_rubrics_comments(a_course, submission, a_levels)
            l_hover += "<br>"
        y_hover.append(l_hover)
        if l_perspective.show_flow:
            y_submission.append(submission_sequence.flow)
        else:
            y_submission.append(cum_score)

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
    if l_perspective.show_flow:
        a_fig.update_yaxes(title_text="Voortgang", range=[0, 1], dtick=1, row=a_row, col=a_col)
    else:
        a_fig.update_yaxes(title_text="Punten", range=[0, l_assignment_group.total_points], row=a_row, col=a_col)
    a_fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester], row=a_row, col=a_col)
    return {"x": x_submission, "y": y_submission}


def remove_assignment(a_assignment_sequences, a_submission_sequence):
    for i in range(0, len(a_assignment_sequences)):
        if a_assignment_sequences[i].id == a_submission_sequence.assignment_id:
            del a_assignment_sequences[i]
            return a_assignment_sequences
    return a_assignment_sequences


def plot_overall_peilingen(a_fig, a_row, a_col, a_start, a_course, a_peiling, a_levels):
    if "beoordeling" in a_peiling.assignment_name.lower():
        # print(a_labels_colors.level_series[a_start.grade_levels].levels["-1"].color)
        label = a_levels.level_series[a_start.grade_levels].levels[str(int(a_peiling.score))].label
        color = a_levels.level_series[a_start.grade_levels].levels[str(int(a_peiling.score))].color
    else:
        label = a_levels.level_series[a_start.level_moments.levels].levels[str(int(a_peiling.score))].label
        color = a_levels.level_series[a_start.level_moments.levels].levels[str(int(a_peiling.score))].color
    if a_peiling.score <= 0:
        y_niveau = [0.2]
    else:
        y_niveau = [a_peiling.score]
    x_labels = [a_peiling.assignment_name]
    y_hover = get_hover_peiling(a_peiling, a_start, a_course, a_levels)
    a_fig.add_trace(go.Bar(x=x_labels, y=y_niveau,
                           name="Hoi",
                           hoverinfo="text",
                           hovertext=y_hover,
                           hoverlabel=hover_style,
                           text=label,
                           marker=dict(color=color)), row=a_row, col=a_col)
    a_fig.update_yaxes(title_text="Niveau", range=[0, 3.5], dtick=1, row=a_row, col=a_col)


def plot_perspective(a_row, a_col, a_fig, a_start, a_course, a_perspective, a_peil_construction,
                     a_actual_day, a_actual_date, a_levels):
    # slechts één assignment_group
    assignment_group = a_course.find_assignment_group(a_perspective.assignment_groups[0])
    if assignment_group is None:
        print("BPP01 - could not find assignment_group", a_perspective.assignment_groups[0])
        return
    show_points = a_course.find_perspective_by_assignment_group(assignment_group.id).show_points

    plot_bandbreedte_colored(a_row, a_col, a_fig, a_course.days_in_semester, assignment_group.bandwidth, a_course.find_perspective_by_name(a_perspective.name).show_flow, assignment_group.total_points)
    if a_start.level_moments is not None and len(a_peil_construction) > 0:
        # print("BPP02 ", a_perspective.name, a_peil_construction)
        plot_progress(a_row, a_col, a_fig, a_start, a_course, a_peil_construction[a_perspective.name], a_levels)
    plot_day_bar(a_row, a_col, a_fig, a_start, assignment_group.total_points, a_actual_day, a_actual_date, a_perspective.progress, a_levels, show_points, a_perspective.sum_score )
    plot_submissions(a_row, a_col, a_fig, a_start, a_course, a_perspective, a_levels)
    assignment_sequences = assignment_group.assignment_sequences[:]
    # for submission_sequence in a_perspective.submission_sequences:
    #     assignment_sequences = remove_assignment(assignment_sequences, submission_sequence)
    print("BPP09 -", a_perspective.name, "assignment_group.assignment_sequences",  len(assignment_group.assignment_sequences))
    plot_future_assignments(a_row, a_col, a_fig, a_start, show_points, assignment_group.assignment_sequences, a_levels)

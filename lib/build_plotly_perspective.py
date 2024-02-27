import copy
import textwrap

from lib.lib_bandwidth import calc_dev
from lib.lib_date import date_to_day, get_date_time_loc
from lib.lib_plotly import get_marker_size, fraction_to_level, hover_style, fraction_to_bin_level, get_score_bin_dict
import plotly.graph_objs as go

from lib.lib_submission import NOT_GRADED, NO_DATA


def get_hover(a_peil_submissions, a_start, a_course, a_labels_colors):
    score = 0.1
    hover = NO_DATA
    if a_peil_submissions:
        if a_peil_submissions.graded:
            score = a_peil_submissions.score + 1
        if "beoordeling".lower() in a_peil_submissions.assignment_name.lower():
            hover = "<b>"+a_peil_submissions.assignment_name + "</b> " + a_labels_colors.level_series[a_start.grade_levels].levels[str(int(score-1))].label
        else:
            hover = "<b>"+a_peil_submissions.assignment_name + "</b> " + a_labels_colors.level_series[a_start.progress_levels].levels[str(int(score-1))].label
        for comment in a_peil_submissions.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
    return hover


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


def plot_progress(a_row, a_col, a_fig, a_start, a_course, a_perspective, a_labels_colors):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': [], 'size': []}
    for pleiling in a_perspective:
        series['y'].append(0)
        if pleiling['submission']:
            #Heeft beoordeling
            series['size'].append(get_marker_size(True)+2)
            series['hover'].append(get_hover(pleiling['submission'], a_start, a_course, a_labels_colors))
            series['x'].append(date_to_day(a_start.start_date, pleiling['submission'].submitted_date))
            if "beoordeling" in pleiling['assignment'].name.lower():
                series['color'].append(a_labels_colors.level_series[a_start.grade_levels].levels[str(int(pleiling['submission'].score))].color)
            else:
                # print(str(int(pleiling['submission'].score)))
                series['color'].append(a_labels_colors.level_series[a_start.progress_levels].levels[str(int(pleiling['submission'].score))].color)
        else:
            #Heeft nog geen beoordeling
            series['size'].append(get_marker_size(False)+2)
            series['hover'].append("<b>"+pleiling['assignment'].name + "</b> " + get_date_time_loc(pleiling['assignment'].assignment_date))
            series['x'].append(date_to_day(a_start.start_date, pleiling['assignment'].assignment_date))
            if "beoordeling" in pleiling['assignment'].name.lower():
                series['color'].append(a_labels_colors.level_series[a_start.grade_levels].levels["-1"].color)
            else:
                series['color'].append(a_labels_colors.level_series[a_start.progress_levels].levels["-1"].color)
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


def plot_open_assignments(a_row, a_col, a_fig, a_start, a_course, a_assignments, a_labels_colors):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': []}

    for assignment in a_assignments:
        series['size'].append(get_marker_size(False))
        series['x'].append(date_to_day(a_start.start_date, assignment.assignment_date))
        series['y'].append(0)
        series['color'].append(a_labels_colors.level_series[a_start.grade_levels].levels["-1"].color)
        # if assignment.points == 1:
        #     PUNTEN = " punt"
        # else:
        #     PUNTEN = " punten"
        # "+str(assignment.points)+PUNTEN+",
        series['hover'].append("<b>"+assignment.name + "</b> deadline " + get_date_time_loc(assignment.assignment_date))
    a_fig.add_trace(
        go.Scatter(
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
        ),
        row=a_row, col=a_col
    )
    return


def plot_day_bar(a_row, a_col, a_fig, a_start, a_total_points, a_actual_day, a_actual_date, a_progress, a_sum_score, a_labels_colors):
    if a_total_points <= 0:
        return
    l_label = a_labels_colors.level_series[a_start.progress_levels].levels[str(a_progress)].label
    l_color = a_labels_colors.level_series[a_start.progress_levels].levels[str(a_progress)].color
    a_fig.add_trace(
        go.Scatter(
            x=[a_actual_day, a_actual_day+2, a_actual_day+2, a_actual_day, a_actual_day],
            y=[0, 0, a_total_points, a_total_points, 0],
            fill="toself",
            mode='lines',
            name='',
            hoverlabel=hover_style,
            text=f"<b>{l_label}</b>,<br>dag {a_actual_day} in onderwijsperiode [{a_actual_date}]", #,<br>{int(a_sum_score)} punt(en)
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

def plot_bandbreedte_fixed(a_row, a_col, a_fig, a_days):
    band_lower = calc_dev(a_days, 14, 0, 0, 0.3)
    band_upper = calc_dev(a_days, 14, 0, 0, 0.7)
    l_days = calc_dev(a_days, 14, 0, 1, 0)
    a_fig.add_trace(
        go.Scatter(
            x=l_days + l_days[::-1],  # x, then x reversed
            y=band_upper + band_lower[::-1],  # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ),
        row=a_row, col=a_col
    )

def plot_bandbreedte(a_row, a_col, a_fig, a_assignment_group):
    if a_assignment_group.total_points <= 0:
        return
    if a_assignment_group.bandwidth is None:
        return
    # teken bandbreedte
    a_fig.add_trace(
        go.Scatter(
            x=a_assignment_group.bandwidth.days + a_assignment_group.bandwidth.days[::-1],  # x, then x reversed
            y=a_assignment_group.bandwidth.uppers + a_assignment_group.bandwidth.lowers[::-1],  # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ),
        row=a_row, col=a_col
    )


def plot_submissions(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_labels_colors):
    score_bin_dict = get_score_bin_dict(a_instances)
    x_submission = [0]
    y_submission = [0]
    y_hover = ['<b>Start</b> '+get_date_time_loc(a_start.start_date)]
    y_colors = [a_labels_colors.level_series[a_start.progress_levels].levels["1"].color]
    y_size = [get_marker_size(False)]
    cum_score = 0
    l_last_graded_day = 0
    l_submissions = sorted(a_perspective.submissions, key=lambda s: s.submitted_date)
    for submission in l_submissions:
        y_size.append(get_marker_size(submission.graded))
        l_day = date_to_day(a_start.start_date, submission.submitted_date)
        x_submission.append(l_day)
        # if submission.points == 1:
        #     PUNTEN = " punt"
        # else:
        #     PUNTEN = " punten"
        #+str(submission.points)+PUNTEN
        l_hover = "<b>"+submission.assignment_name + "</b> deadline " + get_date_time_loc(submission.assignment_date)
        if submission.graded:
            if l_day > l_last_graded_day:
                l_last_graded_day = l_day
            if a_perspective.name == a_start.attendance_perspective:
                cum_score = submission.flow
            else:
                cum_score += submission.score
            if submission.points == 0:
                submission.points = 1
            if submission.points <= 1.1:
                y_colors.append(score_bin_dict[a_perspective.name][fraction_to_bin_level(submission.score / submission.points)]['color'])
                l_hover += "<br><b>" + score_bin_dict[a_perspective.name][fraction_to_bin_level(submission.score / submission.points)]['niveau'] + "</b>, score: " + str(submission.score) + " [" + get_date_time_loc(submission.submitted_date) + "]"
            elif a_perspective.name == a_start.attendance_perspective:
                # print(submission.flow, submission.score, submission.points)
                y_colors.append(a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(int(submission.score))].color)
                l_label = a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(int(submission.score))].label
                l_hover += "<br><b>" + l_label + "</b>, flow: " + str(submission.flow) + " score: " + str(submission.score) + " [" + str(submission.points) + "]" + " - " + get_date_time_loc(submission.submitted_date)
            else:
                level = fraction_to_level(submission.score / submission.points)
                y_colors.append(a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].color)
                l_label = a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].label
                # score: " + str(submission.score) + " [" + str(submission.points) + "]" + "
                l_hover += "<br><b>" + l_label + "</b> ingeleverd " + get_date_time_loc(submission.submitted_date)
        else:
            y_colors.append(a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels["-2"].color)
            l_hover += "<br><b>" + NOT_GRADED + "</b> ingeleverd " + get_date_time_loc(submission.submitted_date)
        for comment in submission.comments:
            l_hover += "<br><b>"+comment.author_name+"</b>" + get_date_time_loc(comment.date)
            value = comment.comment
            wrapper = textwrap.TextWrapper(width=125)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                l_hover += "<br>" + line
        y_submission.append(cum_score)
        y_hover.append(l_hover)

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
    a_fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester], row=a_row, col=a_col)
    return {"x": x_submission, "y": y_submission}


def plot_levels(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_labels_colors):
    # score_bin_dict = get_score_bin_dict(a_instances)
    x_submission = [0]
    y_submission = [0.5]
    y_hover = ['<b>Start</b> '+get_date_time_loc(a_start.start_date)]
    y_colors = [a_labels_colors.level_series[a_start.progress_levels].levels["1"].color]
    y_size = [get_marker_size(False)]
    # cum_score = 0
    l_last_graded_day = 0
    l_submissions = sorted(a_perspective.submissions, key=lambda s: s.submitted_date)
    for submission in l_submissions:
        y_size.append(get_marker_size(submission.graded))
        l_day = date_to_day(a_start.start_date, submission.submitted_date)
        x_submission.append(l_day)
        l_hover = "<b>"+submission.assignment_name + "</b> deadline " + get_date_time_loc(submission.assignment_date)
        if submission.graded:
            if l_day > l_last_graded_day:
                l_last_graded_day = l_day
            level = fraction_to_level(submission.score / submission.points)
            y_colors.append(a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].color)
            l_label = a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].label
            l_hover += "<br><b>" + l_label + "</b> ingeleverd " + get_date_time_loc(submission.submitted_date)
        else:
            y_colors.append(a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels["-2"].color)
            l_hover += "<br><b>" + NOT_GRADED + "</b> ingeleverd " + get_date_time_loc(submission.submitted_date)
        for comment in submission.comments:
            l_hover += "<br><b>"+comment.author_name+"</b>" + get_date_time_loc(comment.date)
            value = comment.comment
            wrapper = textwrap.TextWrapper(width=125)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                l_hover += "<br>" + line
        y_submission.append(submission.flow)
        y_hover.append(l_hover)

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
    a_fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester], row=a_row, col=a_col)
    return {"x": x_submission, "y": y_submission}


def remove_assignment(a_assignments, a_submission):
    for i in range(0, len(a_assignments)):
        if a_assignments[i].id == a_submission.assignment_id:
            del a_assignments[i]
            return a_assignments
    return a_assignments


def plot_perspective(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_peil_construction,
                     a_actual_day, a_actual_date, a_labels_colors):
    # slechts één assignment_group
    assignment_group = a_course.find_assignment_group(a_perspective.assignment_groups[0])
    if assignment_group is None:
        print("could not find assignment_group", a_perspective.assignment_groups[0])
        return
    l_assignments = assignment_group.assignments[:]
    l_missed_submissions = []
    for l_submission in a_perspective.submissions:
        l_assignments = remove_assignment(l_assignments, l_submission)
    # print(a_perspective.name)
    plot_open_assignments(a_row, a_col, a_fig, a_start, a_course, l_assignments, a_labels_colors)
    # a_perspective.submissions = a_perspective.submissions + l_missed_submissions
    if a_start.progress_perspective is not None:
        plot_progress(a_row, a_col, a_fig, a_start, a_course, a_peil_construction[a_perspective.name], a_labels_colors)
    # print(a_perspective.name, a_perspective.progress, a_perspective.sum_score)
    if a_perspective.name == "team" or a_perspective.name == "gilde":
        plot_day_bar(a_row, a_col, a_fig, a_start, 1, a_actual_day, a_actual_date,
                     a_perspective.progress, a_perspective.sum_score, a_labels_colors)
        plot_bandbreedte_fixed(a_row, a_col, a_fig, a_course.days_in_semester)
        plot_levels(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_labels_colors)
        a_fig.update_yaxes(title_text="Voortgang", range=[0, 1], row=a_row, col=a_col)
    elif a_perspective.name == a_start.attendance_perspective:
        plot_day_bar(a_row, a_col, a_fig, a_start, assignment_group.total_points, a_actual_day, a_actual_date,
                     a_perspective.progress, a_perspective.sum_score, a_labels_colors)
        plot_bandbreedte(a_row, a_col, a_fig, assignment_group)
        plot_submissions(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_labels_colors)
        a_fig.update_yaxes(title_text="Percentage aanwezig", range=[0, assignment_group.total_points], row=a_row, col=a_col)
    else:
        plot_day_bar(a_row, a_col, a_fig, a_start, assignment_group.total_points, a_actual_day, a_actual_date,
                     a_perspective.progress, a_perspective.sum_score, a_labels_colors)
        plot_bandbreedte(a_row, a_col, a_fig, assignment_group)
        plot_submissions(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_labels_colors)
        a_fig.update_yaxes(title_text="Punten", range=[0, assignment_group.total_points], row=a_row, col=a_col)
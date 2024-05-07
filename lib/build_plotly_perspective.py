import copy
import textwrap

from lib.lib_bandwidth import calc_dev
from lib.lib_date import date_to_day, get_date_time_loc
from lib.lib_plotly import get_marker_size, fraction_to_level3, hover_style, fraction_to_bin_level, get_score_bin_dict
import plotly.graph_objs as go

from lib.lib_submission import NOT_GRADED, NO_DATA

POINTS = True
NO_POINTS = False


def get_hover(a_peil_submissions, a_start, a_course, a_labels_colors):
    score = 0.1
    hover = NO_DATA
    if a_peil_submissions:
        if a_peil_submissions.graded:
            score = a_peil_submissions.score + 1
        if "beoordeling".lower() in a_peil_submissions.assignment_name.lower():
            hover = "<b>"+a_peil_submissions.assignment_name + "</b> " + a_labels_colors.level_series[a_start.grade_levels].levels[str(int(score-1))].label
        else:
            hover = "<b>"+a_peil_submissions.assignment_name + "</b> " + a_labels_colors.level_series[a_start.progress.levels].levels[str(int(score-1))].label
        for comment in a_peil_submissions.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
    return hover


def get_hover_grade(points, a_labels_colors, a_course, a_perspective, level, submission):
    if submission.graded:
        l_label = a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].label
        if points:
            return "<br><b>" + l_label + "</b>, score: " + str(submission.score) + " ingeleverd " + get_date_time_loc(submission.submitted_date)+"<br>Beoordeeld door "+str(submission.grader_name)
        else:
            return "<br><b>" + l_label + "</b> ingeleverd " + get_date_time_loc(submission.submitted_date)+"<br>Beoordeeld door "+str(submission.grader_name)
    else:
        return "<br><b>" + NOT_GRADED + "</b> ingeleverd " + get_date_time_loc(submission.submitted_date)


def get_hover_comments(submission):
    l_hover = ""
              # '<br><a target="_blank" href="https://canvas.hu.nl/courses/39869/gradebook/speed_grader?assignment_id=298259&amp;student_id=226811">Naar inzending</a>'
    for comment in submission.comments:
        l_hover += "<br><b>" + comment.author_name + "</b> " + get_date_time_loc(comment.date)
        value = comment.comment
        wrapper = textwrap.TextWrapper(width=125)
        word_list = wrapper.wrap(text=value)
        for line in word_list:
            l_hover += "<br>" + line
    return l_hover


def get_hover_rubrics(course, submission):
    if len(submission.rubrics) == 0:
        return ""
    l_hover = "<br><b>Criteria:</b>"
    for criterion_score in submission.rubrics:
        criterion = course.find_assignment(submission.assignment_id).get_criterion(criterion_score.id)
        if criterion_score.rating_id:
            l_hover += "<br>- " + criterion.description + " <b>" + criterion.get_rating(criterion_score.rating_id).description + "</b>"
        else:
            # if criterion_score.score:
                if criterion_score.score == 0:
                    l_hover += "<br>- " + criterion.description + " <b>Niet zichtbaar</b>"
                else:
                    l_hover += "<br>- " + criterion.description + " <b>"+str(criterion_score.score)+"</b>"
            # else:
            #     l_hover += "<br>- " + criterion.description + " <b>Geen waardering</b>"

        value = criterion_score.comment
        wrapper = textwrap.TextWrapper(width=125)
        word_list = wrapper.wrap(text=value)
        for line in word_list:
            l_hover += "<br>" + line
    return l_hover


def get_hover_assignment(points, data_point):
    if "Assignment" in str(type(data_point)):
        assignment = data_point
        if points:
            if assignment.points == 1:
                PUNTEN = " punt"
            else:
                PUNTEN = " punten"
            return "<b>" + assignment.name + "</b>, " + str(assignment.points) + PUNTEN + ", deadline " + get_date_time_loc(assignment.assignment_date)
        else:
            return "<b>" + assignment.name + "</b>, deadline " + get_date_time_loc(assignment.assignment_date)
    else:
        submission = data_point
        if points:
            if submission.points == 1:
                PUNTEN = " punt"
            else:
                PUNTEN = " punten"
            return "<b>" + submission.assignment_name + "</b>, " + str(submission.points) + PUNTEN + ", deadline " + get_date_time_loc(submission.submitted_date)
        else:
            return "<b>" + submission.assignment_name + "</b>, deadline " + get_date_time_loc(submission.assignment_date)



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
                series['color'].append(a_labels_colors.level_series[a_start.progress.levels].levels[str(int(pleiling['submission'].score))].color)
        else:
            #Heeft nog geen beoordeling
            series['size'].append(get_marker_size(False)+2)
            series['hover'].append("<b>"+pleiling['assignment'].name + "</b> " + get_date_time_loc(pleiling['assignment'].assignment_date))
            series['x'].append(date_to_day(a_start.start_date, pleiling['assignment'].assignment_date))
            if "beoordeling" in pleiling['assignment'].name.lower():
                # print(a_labels_colors.level_series[a_start.grade_levels].levels["-1"].color)
                series['color'].append(a_labels_colors.level_series[a_start.grade_levels].levels["-1"].color)
            else:
                # print(a_labels_colors.level_series[a_start.progress_levels].levels["-1"].color)
                series['color'].append(a_labels_colors.level_series[a_start.progress.levels].levels["-1"].color)
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


def plot_open_assignments(a_row, a_col, a_fig, a_start, a_strategy, a_assignments, a_labels_colors):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': []}

    for assignment in a_assignments:
        series['size'].append(get_marker_size(False))
        series['x'].append(date_to_day(a_start.start_date, assignment.assignment_date))
        series['y'].append(0)
        series['color'].append(a_labels_colors.level_series[a_start.grade_levels].levels["-1"].color)
        if a_strategy == "EXP_POINTS" or a_strategy == "LIN_POINTS":
            series['hover'].append(get_hover_assignment(NO_POINTS, assignment))
        else:
            series['hover'].append(get_hover_assignment(POINTS, assignment))

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


def plot_day_bar(a_row, a_col, a_fig, a_start, a_total_points, a_actual_day, a_actual_date, a_progress, a_labels_colors):
    if a_total_points <= 0:
        return
    l_label = a_labels_colors.level_series[a_start.progress.levels].levels[str(a_progress)].label
    l_color = a_labels_colors.level_series[a_start.progress.levels].levels[str(a_progress)].color
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

def plot_bandbreedte_colored(a_row, a_col, a_fig, a_days, a_assignment_group):
    if a_assignment_group.total_points <= 0:
        return
    if a_assignment_group.bandwidth is None:
        return
    band_min = calc_dev(a_days, 0, 0, 0, 0)
    if a_assignment_group.strategy == "EXP_POINTS" or a_assignment_group.strategy == "LIN_POINTS":
        band_lower = calc_dev(a_days, 0, 0, 0, 0.3)
        band_upper = calc_dev(a_days, 0, 0, 0, 0.7)
        band_max = calc_dev(a_days, 0, 0, 0, 1)
        l_days = calc_dev(a_days, 0, 0, 1, 0)
    else:
        band_min = calc_dev(a_days, 0, 0, 0, 0)
        band_upper = a_assignment_group.bandwidth.uppers
        band_lower = a_assignment_group.bandwidth.lowers
        band_max = calc_dev(a_days, 0, 0, 0, a_assignment_group.total_points)
        l_days = a_assignment_group.bandwidth.days

    a_fig.add_trace(
        go.Scatter(
            x=l_days + l_days[::-1],  # x, then x reversed
            y=band_max + band_upper[::-1],  # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(7, 107, 32, 0.5)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ),
        row=a_row, col=a_col
    )
    a_fig.add_trace(
        go.Scatter(
            x=l_days + l_days[::-1],  # x, then x reversed
            y=band_upper + band_lower[::-1],  # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(114, 232, 93, 0.5)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ),
        row=a_row, col=a_col
    )
    a_fig.add_trace(
        go.Scatter(
            x=l_days + l_days[::-1],  # x, then x reversed
            y=band_lower + band_min[::-1],  # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(232, 117, 2, 0.5)',
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


def plot_submissions_points(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_labels_colors):
    score_bin_dict = get_score_bin_dict(a_instances)
    x_submission = [0]
    y_submission = [0]
    y_hover = ['<b>Start</b> '+get_date_time_loc(a_start.start_date)]
    y_colors = [a_labels_colors.level_series[a_start.progress.levels].levels["-1"].color]
    y_size = [get_marker_size(False)]
    cum_score = 0
    l_last_graded_day = 0
    l_submissions = sorted(a_perspective.submissions, key=lambda s: s.submitted_day)
    for submission in l_submissions:
        y_size.append(get_marker_size(submission.graded))
        x_submission.append(submission.submitted_day)
        l_hover = get_hover_assignment(POINTS, submission)
        if submission.graded:
            if submission.submitted_day > l_last_graded_day:
                l_last_graded_day = submission.submitted_day
            if a_perspective.name == a_start.attendance_perspective:
                cum_score = submission.flow
            else:
                cum_score += submission.score
            if submission.points == 0:
                submission.points = 1
            if submission.points <= 1.1:
                y_colors.append(score_bin_dict[a_perspective.name][fraction_to_bin_level(submission.score / submission.points)]['color'])
                level = score_bin_dict[a_perspective.name][fraction_to_bin_level(submission.score / submission.points)]['niveau']
                l_hover += "<br><b>" + level + "</b>, score: " + str(submission.score) + ", ingeleverd " + get_date_time_loc(submission.submitted_date)
                l_hover += get_hover_grade(POINTS, a_labels_colors, a_course, a_perspective, level, submission)
            elif a_perspective.name == a_start.attendance_perspective:
                # print(submission.flow, submission.score, submission.points)
                y_colors.append(a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(int(submission.score))].color)
                l_label = a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(int(submission.score))].label
                l_hover += "<br><b>" + l_label + "</b>, score: " + str(submission.score) + ", datum " + get_date_time_loc(submission.submitted_date)
            else:
                level = fraction_to_level3(submission.score / submission.points)
                y_colors.append(a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].color)
                l_hover += get_hover_grade(POINTS, a_labels_colors, a_course, a_perspective, level, submission)
        else:
            y_colors.append(a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels["-2"].color)
            l_hover += "<br><b>" + NOT_GRADED + "</b> ingeleverd " + get_date_time_loc(submission.submitted_date)
        l_hover += get_hover_comments(submission)
        l_hover += get_hover_rubrics(a_course, submission)
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

def plot_not_graded_submission(a_row, a_col, a_fig, a_course, a_perspective, a_labels_colors):
    # score_bin_dict = get_score_bin_dict(a_instances)
    x_submission = []
    y_submission = []
    y_hover = []
    y_colors = []
    y_size = []
    l_submissions = sorted(a_perspective.submissions, key=lambda s: s.submitted_day)
    for submission in l_submissions:
        if not submission.graded:
            y_size.append(get_marker_size(submission.graded))
            x_submission.append(submission.submitted_day)
            l_hover = get_hover_assignment(NO_POINTS, submission)
            y_colors.append(
                a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels["-2"].color)
            l_hover += "<br><b>" + NOT_GRADED + "</b> ingeleverd " + get_date_time_loc(submission.submitted_date)
            l_hover += get_hover_comments(submission)
            y_submission.append(submission.flow)
            y_hover.append(l_hover)

    a_fig.add_trace(
        go.Scatter(
            x=x_submission,
            y=y_submission,
            hoverinfo="text",
            hovertext=y_hover,
            mode='markers',
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


def plot_submissions_no_points(a_row, a_col, a_fig, a_start, a_course, a_perspective, a_labels_colors):
    x_submission = [0]
    y_submission = [0.5]
    y_hover = ['<b>Start</b> '+get_date_time_loc(a_start.start_date)]
    y_colors = [a_labels_colors.level_series[a_start.progress.levels].levels["-1"].color]
    y_size = [get_marker_size(False)]
    # cum_score = 0
    l_last_graded_day = 0
    l_submissions = sorted(a_perspective.submissions, key=lambda s: s.submitted_day)
    for submission in l_submissions:
        if submission.graded:
            y_size.append(get_marker_size(submission.graded))
            x_submission.append(submission.submitted_day)
            l_hover = get_hover_assignment(NO_POINTS, submission)
            if submission.submitted_day > l_last_graded_day:
                l_last_graded_day = submission.submitted_day
            level = fraction_to_level3(submission.score / submission.points)
            y_colors.append(a_labels_colors.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].color)
            l_hover += get_hover_grade(NO_POINTS, a_labels_colors, a_course, a_perspective, level, submission)
            l_hover += get_hover_comments(submission)
            l_hover += get_hover_rubrics(a_course, submission)
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
    for l_submission in a_perspective.submissions:
        l_assignments = remove_assignment(l_assignments, l_submission)
    plot_bandbreedte_colored(a_row, a_col, a_fig, a_course.days_in_semester, assignment_group)
    if a_start.progress is not None:
        plot_progress(a_row, a_col, a_fig, a_start, a_course, a_peil_construction[a_perspective.name], a_labels_colors)
    if assignment_group.strategy == "EXP_POINTS" or assignment_group.strategy == "LIN_POINTS":
        plot_day_bar(a_row, a_col, a_fig, a_start, 1, a_actual_day, a_actual_date, a_perspective.progress, a_labels_colors)
        plot_submissions_no_points(a_row, a_col, a_fig, a_start, a_course, a_perspective, a_labels_colors)
        plot_not_graded_submission(a_row, a_col, a_fig, a_course, a_perspective, a_labels_colors)
        a_fig.update_yaxes(title_text="Voortgang", range=[0, 1], dtick=1, row=a_row, col=a_col)
        a_fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester], row=a_row, col=a_col)
    elif a_perspective.name == a_start.attendance_perspective:
        plot_day_bar(a_row, a_col, a_fig, a_start, assignment_group.total_points, a_actual_day, a_actual_date,
                     a_perspective.progress, a_perspective.sum_score, a_labels_colors)
        plot_submissions_points(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_labels_colors)
        a_fig.update_yaxes(title_text="Percentage aanwezig", range=[0, assignment_group.total_points], row=a_row, col=a_col)
        a_fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester], row=a_row, col=a_col)
    else:
        plot_day_bar(a_row, a_col, a_fig, a_start, assignment_group.total_points, a_actual_day, a_actual_date,
                     a_perspective.progress, a_labels_colors)
        plot_submissions_points(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_labels_colors)
        a_fig.update_yaxes(title_text="Punten", range=[0, assignment_group.total_points], row=a_row, col=a_col)
    plot_open_assignments(a_row, a_col, a_fig, a_start, assignment_group.strategy, l_assignments, a_labels_colors)

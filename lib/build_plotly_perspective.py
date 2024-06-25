import copy
import textwrap
import plotly.graph_objs as go

from lib.lib_bandwidth import calc_dev
from lib.lib_date import date_to_day, get_date_time_loc
from lib.lib_plotly import get_marker_size, hover_style

from lib.lib_submission import NOT_GRADED, NO_DATA


def get_punten_str(points):
    if points == 1:
        return " punt"
    else:
        return " punten"


def get_hover_assignment(points, data_point):
    if "Assignment" in str(type(data_point)):
        # geen oplevering
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
        assignment_criterion = course.find_assignment(submission.assignment_id).get_criterion(criterion_score.id)
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
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': [], 'size': []}
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


def plot_open_assignments(a_row, a_col, a_fig, a_start, a_show_points, a_assignments, a_levels):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': []}

    for assignment in a_assignments:
        series['size'].append(get_marker_size(False))
        series['x'].append(date_to_day(a_start.start_date, assignment.assignment_date))
        series['y'].append(0)
        series['color'].append(a_levels.level_series[a_start.grade_levels].levels["-1"].color)
        series['hover'].append(get_hover_assignment(a_show_points, assignment))

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
    if a_row == 0:
        a_fig.add_trace(open_assignments)
    else:
        a_fig.add_trace(open_assignments, row=a_row, col=a_col)
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


def plot_bandbreedte_colored(a_row, a_col, a_fig, a_days, a_assignment_group, a_flow):
    if a_assignment_group.total_points <= 0:
        return
    if a_assignment_group.bandwidth is None:
        return
    band_min = calc_dev(a_days, 0, 0, 0, 0)
    if a_flow:
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

    boven_niveau = go.Scatter(
        x=l_days + l_days[::-1],  # x, then x reversed
        y=band_max + band_upper[::-1],  # upper, then lower reversed
        fill='toself',
        fillcolor='rgba(7, 107, 32, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False
    )

    op_niveau = go.Scatter(
        x=l_days + l_days[::-1],  # x, then x reversed
        y=band_upper + band_lower[::-1],  # upper, then lower reversed
        fill='toself',
        fillcolor='rgba(114, 232, 93, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False
    )

    onder_niveau = go.Scatter(
        x=l_days + l_days[::-1],  # x, then x reversed
        y=band_lower + band_min[::-1],  # upper, then lower reversed
        fill='toself',
        fillcolor='rgba(232, 117, 2, 0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False
    )
    if a_row == 0:
        a_fig.add_trace(boven_niveau)
        a_fig.add_trace(op_niveau)
        a_fig.add_trace(onder_niveau)
    else:
        a_fig.add_trace(boven_niveau, row=a_row, col=a_col)
        a_fig.add_trace(op_niveau, row=a_row, col=a_col)
        a_fig.add_trace(onder_niveau, row=a_row, col=a_col)


def plot_submissions(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_levels):
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
    for submission in a_perspective.submissions:
        y_size.append(get_marker_size(submission.graded))
        x_submission.append(submission.assignment_day)
        l_hover = get_hover_assignment(l_perspective.show_points, submission)
        if submission.graded:
            cum_score += submission.score
            if submission.points == 0:
                submission.points = 1
            level = a_levels.level_series[a_course.perspectives[a_perspective.name].levels].get_level_by_fraction(submission.score / submission.points)
            y_colors.append(a_levels.level_series[a_course.perspectives[a_perspective.name].levels].levels[str(level)].color)
            l_hover += get_hover_grade(a_levels, a_course, a_perspective, level, submission)
        else:
            y_colors.append(a_levels.level_series[a_course.perspectives[a_perspective.name].levels].levels["-2"].color)
            l_hover += get_hover_grade(a_levels, a_course, a_perspective, "", submission)
        l_hover += get_hover_comments(submission.comments)
        l_hover += get_hover_rubrics_comments(a_course, submission, a_levels)
        y_hover.append(l_hover)
        if l_perspective.show_flow:
            y_submission.append(submission.flow)
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
    elif a_perspective.name == "attendance":
        a_fig.update_yaxes(title_text="Percentage aanwezig", range=[0, l_assignment_group.total_points], row=a_row, col=a_col)
    else:
        a_fig.update_yaxes(title_text="Punten", range=[0, l_assignment_group.total_points], row=a_row, col=a_col)
    a_fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester], row=a_row, col=a_col)
    return {"x": x_submission, "y": y_submission}


def remove_assignment(a_assignments, a_submission):
    for i in range(0, len(a_assignments)):
        if a_assignments[i].id == a_submission.assignment_id:
            del a_assignments[i]
            return a_assignments
    return a_assignments


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


def plot_perspective(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_peil_construction,
                     a_actual_day, a_actual_date, a_levels):
    # slechts één assignment_group
    assignment_group = a_course.find_assignment_group(a_perspective.assignment_groups[0])
    if assignment_group is None:
        print("BPP01 - could not find assignment_group", a_perspective.assignment_groups[0])
        return
    show_points = a_course.find_perspective_by_assignment_group(assignment_group.id).show_points
    l_assignments = assignment_group.assignments[:]
    for l_submission in a_perspective.submissions:
        l_assignments = remove_assignment(l_assignments, l_submission)
    plot_bandbreedte_colored(a_row, a_col, a_fig, a_course.days_in_semester, assignment_group, a_course.find_perspective_by_name(a_perspective.name).show_flow)
    if a_start.level_moments is not None and len(a_peil_construction) > 0:
        # print("BPP02 ", a_perspective.name, a_peil_construction)
        plot_progress(a_row, a_col, a_fig, a_start, a_course, a_peil_construction[a_perspective.name], a_levels)
    plot_day_bar(a_row, a_col, a_fig, a_start, assignment_group.total_points, a_actual_day, a_actual_date, a_perspective.progress, a_levels, show_points, a_perspective.sum_score )
    plot_submissions(a_row, a_col, a_fig, a_instances, a_start, a_course, a_perspective, a_levels)
    plot_open_assignments(a_row, a_col, a_fig, a_start, show_points, l_assignments, a_levels)

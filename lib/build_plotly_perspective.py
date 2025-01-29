import copy
import plotly.graph_objs as go

from lib.build_plotly_generic import plot_bandbreedte_colored
from lib.build_plotly_hover import get_hover_assignment, get_hover_day_bar, get_hover_grade, \
    get_hover_comments, get_hover_rubrics_comments, get_hover_status, get_hover_moment
from lib.lib_date import date_to_day, get_date_time_loc
from lib.lib_plotly import get_marker_size, hover_style
from model.perspective.Status import BEFORE_DEADLINE


def find_submissions(a_student, a_peil_construction):
    if a_peil_construction is None:
        return
    l_peil_construction = copy.deepcopy(a_peil_construction)
    for l_perspective in l_peil_construction.values():
        for peil in l_perspective:
            l_submission = a_student.get_grade_moment(peil['assignment'].id)
            if l_submission is None:
                l_submission = a_student.get_level_moment(peil['assignment'].id)
            if l_submission is not None:
                peil['submission'] = l_submission
    return l_peil_construction



def plot_progress(a_row, a_col, a_fig, a_course, a_perspective, a_level_serie_collection):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': []}
    for peiling in a_perspective:
        series['y'].append(0)
        # print("BPP13 -", a_perspective,  peiling["assignment"], peiling["submission"])
        if peiling['submission'] is not None and peiling['submission'].graded:
            #Heeft submission en beoordeling
            series['size'].append(get_marker_size(True)+2)
            series['hover'].append(get_hover_moment( a_course, peiling['submission'], a_level_serie_collection.level_series[a_course.level_moments.levels]))
            series['x'].append(date_to_day(a_course.start_date, peiling['submission'].submitted_date))
            if "beoordeling" in peiling['assignment'].name.lower():
                series['color'].append(a_level_serie_collection.level_series["grade"].grades[peiling['submission'].grade].color)
            else:
                series['color'].append(a_level_serie_collection.level_series["progress"].grades[peiling['submission'].grade].color)
        else:
            #Heeft nog geen beoordeling
            series['size'].append(get_marker_size(False)+2)
            series['hover'].append("<b>"+peiling['assignment'].name + "</b> " + get_date_time_loc(peiling['assignment'].assignment_date))
            series['x'].append(date_to_day(a_course.start_date, peiling['assignment'].assignment_date))
            if "beoordeling" in peiling['assignment'].name.lower():
                series['color'].append(a_level_serie_collection.level_series["grade"].get_status(BEFORE_DEADLINE).color)
            else:
                series['color'].append(a_level_serie_collection.level_series["progress"].get_status(BEFORE_DEADLINE).color)
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


def plot_assignments(a_row, a_col, a_fig, a_course, a_show_points, a_assignment_sequences, a_levels):
    series = {"color": [], "size": [], "size2": [], 'x': [], 'y': [], 'hover': []}
    cum_points = 0

    for assignment_sequence in a_assignment_sequences:
        cum_points += assignment_sequence.points
        series = {"color": [], "size": [], "size2": [], 'x': [], 'y': [], 'hover': []}
        for assignment in assignment_sequence.assignments:

            series['size'].append(get_marker_size(False))
            series['x'].append(assignment.unlock_day)
            series['y'].append(cum_points)
            # print("PA05 -", a_course.grade_levels)
            # print("PA07 -",a_levels.level_series[a_course.grade_levels].levels["3"].color)
            series['color'].append(a_levels.level_series[a_course.grade_moments.levels].grades["3"].color)
            series['hover'].append(get_hover_assignment(a_show_points, assignment))
            series['size'].append(get_marker_size(True))
            series['x'].append(assignment.assignment_day)
            series['y'].append(cum_points)
            series['color'].append(a_levels.level_series[a_course.grade_moments.levels].grades["0"].color)
            series['hover'].append(get_hover_assignment(a_show_points, assignment))

        open_assignments = go.Scatter(
            x=series['x'],
            y=series['y'],
            hoverinfo="text",
            hovertext=series['hover'],
            mode='lines+markers',
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
        a_fig.add_trace(open_assignments, secondary_y=False)
    return


def plot_future_assignments(a_row, a_col, a_fig,
                            a_course, a_show_points,
                            a_assignment_sequences, a_student_perspective, a_actual_day, a_levels):
    series = {"color": [], "size": [], 'x': [], 'y': [], 'hover': []}
    for assignment_sequence in a_assignment_sequences:
        submission_sequences = a_student_perspective.get_sequence_by_tag(assignment_sequence.tag)
        date, day = assignment_sequence.get_date_day(submission_sequences, a_actual_day)
        if day <= a_actual_day:
            continue
        series['size'].append(get_marker_size(False))
        series['x'].append(day)
        series['y'].append(0)
        series['color'].append(a_levels.level_series[a_course.level_moments.levels].get_status(BEFORE_DEADLINE).color)
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


def plot_day_bar(a_row, a_col, a_fig,
                 a_course, a_total_points, a_actual_day, a_actual_date, a_progress, a_grades, a_show_points, a_show_flow, a_actual_points):
    if a_total_points <= 0:
        return
    if a_show_flow:
        a_total_points = 1
    l_label = a_grades[str(a_progress)].label
    l_color = a_grades[str(a_progress)].color
    l_hover = get_hover_day_bar(l_label, a_actual_day, a_actual_date, a_show_points, a_actual_points)

    a_fig.add_trace(
        go.Scatter(
            x=[a_actual_day, a_actual_day-1, a_actual_day-1, a_actual_day, a_actual_day],
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
        dict(type="rect", x0=a_actual_day-1, x1=a_actual_day, y0=0, y1=a_total_points,
             fillcolor=l_color, line_color=l_color
             ),
        row=a_row,
        col=a_col
    )


def plot_submissions(a_row, a_col, a_fig, a_course, a_perspective, a_level_serie_collection):
    l_assignment_group = a_course.find_assignment_group(a_perspective.assignment_groups[0])
    l_perspective = a_course.find_perspective_by_name(a_perspective.name)
    l_level_serie = a_level_serie_collection.level_series[a_course.perspectives[a_perspective.name].levels]
    x_submission = [0]
    if l_perspective.show_flow:
        y_submission = [0.5]
    else:
        y_submission = [0]
    y_hover = ['<b>Start</b> '+get_date_time_loc(a_course.start_date)]
    y_colors = [a_level_serie_collection.level_series[a_course.level_moments.levels].get_status(BEFORE_DEADLINE).color]
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
            grade = l_level_serie.grades[submission_sequence.get_grade()]
            y_colors.append(grade.color)
        else:
            status = l_level_serie.status[submission_sequence.get_status()]
            y_colors.append(status.color)

        submission_nr = 0
        l_hover = ""
        for submission in submission_sequence.submissions:
            l_hover += get_hover_assignment(l_perspective.show_points, submission)
            if submission.graded:
                grade = l_level_serie.grades[submission.grade]
                l_hover += get_hover_grade(a_course, submission, grade)
            else:
                status = l_level_serie.status[submission.status]
                l_hover += get_hover_status(submission, status)
            l_hover += get_hover_comments(submission.comments)
            if submission.graded:
                grade = l_level_serie.grades[submission.grade]
                l_hover += get_hover_rubrics_comments(a_course, submission, grade)
            if submission_nr < len(submission_sequence.submissions) - 1:
                l_hover += "<br><br>"
        if len(l_hover) > 4000:
            l_hover = l_hover[:4000] + "<br>Te veel commentaar/feedback voor pop-up. Ga naar Canvas voor de complete tekst."

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


def remove_assignment_sequence(a_assignment_sequences, a_submission_sequence):
    for i in range(0, len(a_assignment_sequences)):
        # print("BPP41 -", a_assignment_sequences[i].tag, a_submission_sequence.tag)
        if a_assignment_sequences[i].tag == a_submission_sequence.tag:
            # print("BPP42 - is gelijk", a_assignment_sequences[i].tag, a_submission_sequence.tag)
            lengte = len(a_assignment_sequences)
            del a_assignment_sequences[i]
            # print("BPP43 - assignment_sequences", lengte, len(a_assignment_sequences))
            return a_assignment_sequences
    return a_assignment_sequences


def plot_overall_level_moment(a_row, a_col, a_fig, a_course, a_level_moment, a_levels):
    if a_level_moment.graded:
        label = a_levels.level_series[a_course.level_moments.levels].grades[a_level_moment.grade].label
        color = a_levels.level_series[a_course.level_moments.levels].grades[a_level_moment.grade].color
    else:
        label = a_levels.level_series[a_course.level_moments.levels].get_status(BEFORE_DEADLINE).label
        color = a_levels.level_series[a_course.level_moments.levels].get_status(BEFORE_DEADLINE).color

    if a_level_moment.grade is None:
        y_niveau = [0.2]
    else:
        y_niveau = [a_level_moment.grade]
    x_labels = [a_level_moment.assignment_name]
    y_hover = get_hover_moment(a_course, a_level_moment, a_levels.level_series[a_course.level_moments.levels])
    a_fig.add_trace(go.Bar(x=x_labels, y=y_niveau,
                           name="Hoi",
                           hoverinfo="text",
                           hovertext=y_hover,
                           hoverlabel=hover_style,
                           text=label,
                           marker=dict(color=color)), row=a_row, col=a_col)
    a_fig.update_yaxes(title_text="Niveau", range=[0, 3.5], dtick=1, row=a_row, col=a_col)


def plot_overall_grade_moment(a_row, a_col, a_fig, a_course, a_grade_moment, a_levels):
    if a_grade_moment.graded:
        # print("BPP41 -", a_grade_moment.assignment_name, a_course.grade_moments.name)
        # print("BPP42 -", a_levels.level_series[a_course.grade_moments.levels])
        label = a_levels.level_series[a_course.grade_moments.levels].grades[a_grade_moment.grade].label
        color = a_levels.level_series[a_course.grade_moments.levels].grades[a_grade_moment.grade].color
    else:
        label = a_levels.level_series[a_course.grade_moments.levels].get_status(BEFORE_DEADLINE).label
        color = a_levels.level_series[a_course.grade_moments.levels].get_status(BEFORE_DEADLINE).color

    if a_grade_moment.grade is None:
        y_niveau = [0.2]
    else:
        y_niveau = [int(a_grade_moment.grade)]
    x_labels = [a_grade_moment.assignment_name]
    y_hover = get_hover_moment(a_course, a_grade_moment, a_levels.level_series[a_course.grade_moments.levels])

    a_fig.add_trace(go.Bar(x=x_labels, y=y_niveau,
                           name="Hoi",
                           hoverinfo="text",
                           hovertext=y_hover,
                           hoverlabel=hover_style,
                           text=label,
                           marker=dict(color=color)), row=a_row, col=a_col)
    a_fig.update_yaxes(title_text="Niveau", range=[0, 3.5], dtick=1, row=a_row, col=a_col)


def plot_perspective(a_row, a_col, a_fig, a_course, a_student_perspective, a_level_construction, a_grade_construction,
                     a_actual_day, a_actual_date, a_level_serie_collection):
    # slechts één assignment_group
    assignment_group = a_course.find_assignment_group(a_student_perspective.assignment_groups[0])
    if assignment_group is None:
        print("BPP01 - could not find assignment_group", a_student_perspective.assignment_groups[0], a_student_perspective)
        return
    show_points = a_course.find_perspective_by_assignment_group(assignment_group.id).show_points
    show_flow = a_course.find_perspective_by_assignment_group(assignment_group.id).show_flow
    plot_bandbreedte_colored(a_row, a_col, a_fig, a_course.days_in_semester, assignment_group.bandwidth, show_flow, assignment_group.total_points)
    if a_course.level_moments is not None and len(a_level_construction) > 0:
        # print("BPP02 -", a_student_perspective.name)
        plot_progress(a_row, a_col, a_fig, a_course,
                      a_level_construction[a_student_perspective.name],
                      a_level_serie_collection)
    if a_course.grade_moments is not None and len(a_grade_construction) > 0:
        # print("BPP03 -", a_student_perspective.name)
        plot_progress(a_row, a_col, a_fig, a_course,
                      a_grade_construction[a_student_perspective.name],
                      a_level_serie_collection)

    plot_day_bar(a_row, a_col, a_fig,
                 a_course, assignment_group.total_points, a_actual_day, a_actual_date,
                 a_student_perspective.progress, a_level_serie_collection.level_series["progress"].grades, show_points, show_flow, a_student_perspective.sum_score)

    plot_submissions(a_row, a_col, a_fig, a_course, a_student_perspective, a_level_serie_collection)
    # assignment_sequences = assignment_group.assignment_sequences[:]
    # for submission_sequence in a_student_perspective.submission_sequences:
    #    assignment_sequences = remove_assignment_sequence(assignment_sequences, submission_sequence)
    # # print("BPP09 -", a_perspective.name, "assignment_group.assignment_sequences",  len(assignment_sequences))
    plot_future_assignments(a_row, a_col, a_fig,
                            a_course, show_points,
                            assignment_group.assignment_sequences, a_student_perspective, a_actual_day,
                            a_level_serie_collection)

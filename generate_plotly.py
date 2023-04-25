import math
import textwrap
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from lib.config import start_date, end_date, str_date_to_day, plot_path, score_tabel
from lib.file import read_course_config_start, read_course_config, read_course_results

from lib.translation_table import translation_table

traces = []

timedelta = end_date - start_date
days_in_semester= timedelta.days
print("days_in_semester", days_in_semester)
course_config_start = read_course_config_start()
course_config = read_course_config(course_config_start.course_file_name)
course = read_course_results(course_config_start.results_file_name)

bins_bar = [0, 0.9, 1.9, 2.9, 3.9, 4.9]
labels_bar = ['Leeg', 'Geen', 'Onvoldoende', 'Voldoende', 'Goede']
# Define bar properties
colors_bar = {'Leeg': '#666666',
              'Geen': '#f25829',
              'Onvoldoende': '#f2a529',
              'Voldoende': '#85e043',
              'Goede': '#2bad4e'}


def calc_dev(iterations, a, b, c):
    iteration_list = []
    for x in range(iterations):
        y = a*x*x+b*x+c
        if y < 0:
            y = 0
        iteration_list.append(y)
    return iteration_list

def plot_bandbreedte(a_row, a_col, fig, assignmentGroup):
    if assignmentGroup.total_points <= 0:
        return
    # print("Name:", assignmentGroup.name, "Scale:", assignmentGroup.scale)
    x_time = calc_dev(days_in_semester, 0, 1, 0)
    # bereken bandbreedte
    if assignmentGroup.name == "TEAM":
        # bandbreedte team
        band_lower = calc_dev(days_in_semester, 0.0012, 0.05, -1)
        # band_upper = calc_dev(days_in_semester, 0.002, 0.05, 4)
        band_upper = calc_dev(days_in_semester, 0.001786, 0.05, 8)
        fig.update_yaxes(title_text="Punten", range=[0, 60], row=a_row, col=a_col)
    elif assignmentGroup.name == "GILDE":
        # bandbreedte gilde
        a = 0
        b = assignmentGroup.lower_points / (days_in_semester - 30)
        c = - 30 * b
        band_lower = calc_dev(days_in_semester, a, b, c)
        band_upper = calc_dev(days_in_semester, a, b, c + assignmentGroup.upper_points - assignmentGroup.lower_points)
        fig.update_yaxes(title_text="Punten", range=[0, 20], row=a_row, col=a_col)
    else:
        a = 0
        b = assignmentGroup.lower_points / (days_in_semester - 30)
        c = - 30 * b
        band_lower = calc_dev(days_in_semester, a, b, c)
        band_upper = calc_dev(days_in_semester, a, b, c + assignmentGroup.upper_points - assignmentGroup.lower_points)
        fig.update_yaxes(title_text="Punten", range=[0, assignmentGroup.total_points], row=a_row, col=a_col)

    # teken bandbreedte
    fig.add_trace(
        go.Scatter(
            x=x_time + x_time[::-1],  # x, then x reversed
            y=band_upper + band_lower[::-1],  # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ),
        row=a_row, col=a_col
    )

def plot_submissions(a_row, a_col, fig, submissions):
    x_submission = [0]
    y_submission = [0]
    y_hover = ['Start']
    cum_score = 0
    for submission in submissions:
        x_submission.append(str_date_to_day(submission.submitted_at))
        cum_score += submission.score
        y_submission.append(cum_score)
        hover = submission.assignment_name + "<br>Score: " + str(submission.score)
        for comment in submission.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
        y_hover.append(hover)

    fig.add_trace(
        go.Scatter(
            x=x_submission,
            y=y_submission,
            hoverinfo="text",
            hovertext=y_hover),
        row=a_row, col=a_col
    )
    return {"x": x_submission, "y": y_submission}

def plot_kennis(a_row, a_col, fig, student, role, assignmentGroup):
    x_day = [0]
    y_kennis = [0]
    y_hover = ['Start']
    cum_score = 0
    # y_max_points = assignmentGroup.total_points
    for submission in student.kennis:
        x_day.append(str_date_to_day(submission.submitted_at))
        cum_score += submission.score
        y_kennis.append(cum_score)
        hover = submission.assignment_name + "<br>Score: " + str(submission.score)
        for comment in submission.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
        y_hover.append(hover)

    fig.add_trace(
        go.Scatter(
            x=x_day,
            y=y_kennis,
            hoverinfo="text",
            hovertext=y_hover),
        row=a_row, col=a_col,
    )


def get_bar(a_peilmoment):
    score = 0.1
    hover = "Geen data"
    if a_peilmoment:
        if a_peilmoment.graded:
            score = a_peilmoment.score + 1
        hover = a_peilmoment.assignment_name + " - " + score_tabel[int(score-1)]
        for comment in a_peilmoment.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
    return score, hover

def plot_peilmoment_bar(a_row, a_col, a_fig, a_perspective):
    y_hover = ["", "", ""]
    peilmoment = a_perspective.get_submission(247772)
    team_score, y_hover[0] = get_bar(peilmoment)
    peilmoment = a_perspective.get_submission(247773)
    gilde_score, y_hover[1] = get_bar(peilmoment)
    peilmoment = a_perspective.get_submission(247771)
    kennis_score, y_hover[2] = get_bar(peilmoment)
    #
    a_peil = {'x': ['Team', 'Gilde', 'Kennis'], 'y': [team_score, gilde_score, kennis_score]}
    bins = [0, 0.9, 1.9, 2.9, 3.9, 4.9]
    labels = ['Leeg', 'Geen', 'Onvoldoende', 'Voldoende', 'Goede']
    # Define bar properties
    colors = {'Leeg': '#666666',
              'Geen': '#f25829',
              'Onvoldoende': '#f2a529',
              'Voldoende': '#85e043',
              'Goede': '#2bad4e'}

    # Build dataframe
    df = pd.DataFrame({'y': a_peil['y'],
                       'x': a_peil['x'],
                       'text': y_hover,
                       'label': pd.cut(a_peil['y'], bins=bins, labels=labels)})

    for label, label_df in df.groupby('label'):
        a_fig.add_trace(
            go.Bar(
                x=label_df.x,
                y=label_df.y,
                hoverinfo="text",
                hovertext=label_df.text,
                name=label,
                marker={'color': colors[label]}
            ),
            a_row,
            a_col
        )
    a_fig.update_yaxes(
        showticklabels=False,
        range=[0, 4.5],
        row=a_row,
        col=a_col
    )

def plot_peilmoment(a_row, a_col, a_fig, a_peil):
    # plotting de gauge
    plot_bgcolor = "#fff"
    quadrant_colors = ["#f25829", "#f2a529", "#85e043", "#2bad4e"]
    quadrant_text = ["", "<b>Hoge</b>", "<b>Voldoende</b>", "<b>Onvoldoende</b>", "<b>Geen</b>"]

    n_quadrants = len(quadrant_colors)
    total_reference_moments = 4

    # deel de gauge op in n quadrants (met getallen die niet heel deelbaar zijn door n is het laatste quadrant nu korter)
    gauge_quadrants = list(
        range(0, math.ceil(total_reference_moments + total_reference_moments / n_quadrants),
              math.ceil(total_reference_moments / n_quadrants)))

    gauge = go.Indicator(
        mode="gauge",
        value=a_peil,
        delta={
            'reference': 0,
            'increasing': {
                'color': quadrant_colors[[a_peil > x for x in gauge_quadrants].index(False) - 1],
                'symbol': ''
            }
        },
        gauge={
            'axis': {
                'visible': False,
                'range': [None, total_reference_moments],
                'dtick': math.ceil(total_reference_moments / n_quadrants)
            },
            'bar': {'color': "#555555", 'thickness': 0.3},
            'bgcolor': plot_bgcolor,
            'steps': [
                {'line': {'width': 0}, 'range': [gauge_quadrants[i], gauge_quadrants[i + 1]],
                 'color': quadrant_colors[i]}
                for i in range(len(gauge_quadrants) - 1)],
            'threshold': {
                'line': {'color': "#555555", 'width': 12},
                'thickness': 0.6,
                'value': a_peil}})
    a_fig.add_trace(gauge, a_row, a_col)


def plot_student(course_config, student):
    specs = [[{'type': 'scatter', 'colspan': 2}, None, {'type': 'scatter', 'colspan': 2}, None],
             [{'type': 'scatter', "colspan": 2}, None, {'type': 'bar'}, {'type': 'domain'}]]
    titles = ["Team", "Kennis", "Gilde", "Perspectief", "Voortgang"] #, "Peilmomenten"
    positions = {'team': {'row': 1, 'col': 1}, 'gilde': {'row': 2, 'col': 1}, 'kennis': {'row': 1, 'col': 3}, 'peil': {'row': 2, 'col': 4}}
    fig = make_subplots(rows=2, cols=4, subplot_titles=titles, specs=specs, vertical_spacing=0.15, horizontal_spacing=0.08)
    for perspective in student.perspectives:
        row = positions[perspective.name]['row']
        col = positions[perspective.name]['col']
        if (perspective.name == "peil"):
            plot_peilmoment_bar(2, 3, fig, perspective)
            # Peilmoment overall
            if student.get_peilmoment(247774):
                plot_peilmoment(row, col, fig, student.get_peilmoment(247774).score + 0.5)
            else:
                plot_peilmoment(row, col, fig, 0.1)
        else:
            assigment_group = course_config.find_assignment_group(perspective.assignment_groups[0])
            plot_bandbreedte(row, col, fig, assigment_group)
            plot_submissions(row, col, fig, perspective.submissions)
    #
    # #kennisroute
    # role = student.get_role()
    # plot_kennis(1, 3, fig, student, role, course_config.find_assignment_group_by_role(role))
    # plot_bandbreedte(1, 3, fig, course_config.find_assignment_group_by_role(role))

    fig.update_layout(height=800, width=1200, showlegend=False)
    fig.update_xaxes(title_text="Dagen in semester", range=[0, 150], row=1, col=1)
    fig.update_xaxes(title_text="Dagen in semester", range=[0, 150], row=2, col=1)
    fig.update_xaxes(title_text="Dagen in semester", range=[0, 150], row=1, col=3)
    file_name = plot_path + student.name + ".html"
    asci_file_name = file_name.translate(translation_table)
    print(asci_file_name)
    fig.write_html(asci_file_name, include_plotlyjs="cdn")


for group in course.studentGroups:
    for student in group.students:
        plot_student(course_config, student)


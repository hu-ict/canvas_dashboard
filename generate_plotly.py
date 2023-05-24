import math
import textwrap
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from lib.config import plot_path, score_tabel, date_to_day
from lib.file import read_course_config_start, read_course, read_results

from lib.translation_table import translation_table
from model.Assignment import Assignment

traces = []
course_config_start = read_course_config_start()
days_in_semester = (course_config_start.end_date - course_config_start.start_date).days
print("days_in_semester", days_in_semester)
course = read_course(course_config_start.course_file_name)
results = read_results(course_config_start.results_file_name)

bins_bar = [0, 0.9, 1.9, 2.9, 3.9, 4.9]
# Define bar properties
colors_bar = {'Leeg': '#666666',
              'Geen': '#f25829',
              'Onvoldoende': '#f2a529',
              'Voldoende': '#85e043',
              'Goede': '#2bad4e'}

print(colors_bar.keys())

def calc_dev(iterations, a, b, c):
    iteration_list = []
    for x in range(iterations):
        y = a*x*x+b*x+c
        if y < 0:
            y = 0
        iteration_list.append(y)
    return iteration_list


def peil_contruct():
    peil_perspectives = {}
    for perspective in course.perspectives:
        if perspective.name != course_config_start.peil_perspective:
            peil_perspectives[perspective.name] = []
        else:
            peil_perspective = perspective
    #         print("peil_perspective", peil_perspective)
    # print("peil_perspectives", peil_perspectives)
    assignment_group = course.find_assignment_group(peil_perspective.assignment_groups[0])
    for assignment in assignment_group.assignments:
        for peil_perspective in peil_perspectives:
            if peil_perspective.lower() in assignment.name.lower():
                peil_perspectives[peil_perspective].append(assignment)
    return peil_perspectives

peil_construction = peil_contruct()
for peil in peil_construction:
    print(peil)
    for assignment in peil_construction[peil]:
        print(assignment)

def plot_bandbreedte(a_row, a_col, fig, assignmentGroup):
    if assignmentGroup.total_points <= 0:
        return
    x_time = calc_dev(days_in_semester-14, 0, 1, 0)
    # bereken bandbreedte
    if assignmentGroup.name == "TEAM":
        band_lower = calc_dev(days_in_semester-14, 0.0012, 0.05, -1)
        band_upper = calc_dev(days_in_semester-14, 0.001786, 0.05, 8)
        fig.update_yaxes(title_text="Punten", range=[0, assignmentGroup.total_points], row=a_row, col=a_col)
    else:
        a = 0
        b = assignmentGroup.lower_points / (days_in_semester - 30)
        c = - 30 * b
        band_lower = calc_dev(days_in_semester-14, a, b, c)
        band_upper = calc_dev(days_in_semester-14, a, b, c + assignmentGroup.upper_points - assignmentGroup.lower_points)
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
        x_submission.append(date_to_day(course_config_start.start_date, submission.submitted_at))
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


def get_bar_score(a_peilmoment):
    score = 0.1
    if a_peilmoment:
        if a_peilmoment.graded:
            score = a_peilmoment.score + 1
    return score

def get_bar_hover(a_peilmoment):
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
    return hover

def plot_peilmoment_bar(a_row, a_col, a_fig, a_perspective):
    score = []
    x_ax = []
    y_hover = []
    for perspective in peil_construction:
        for assignment in peil_construction[perspective]:
            submission = a_perspective.get_submission(assignment.id)
            x_ax.append(perspective)
            score.append(get_bar_score(submission))
            if submission:
                y_hover.append(get_bar_hover(submission))
            else:
                y_hover.append(assignment.name+" - geen data")


    # y_hover = ["", "", ""]
    # peilmoment = a_perspective.get_submission(247772)
    # team_score, y_hover[0] = get_bar(peilmoment)
    # peilmoment = a_perspective.get_submission(247773)
    # gilde_score, y_hover[1] = get_bar(peilmoment)
    # peilmoment = a_perspective.get_submission(247771)
    # kennis_score, y_hover[2] = get_bar(peilmoment)
    # Build dataframe
    df = pd.DataFrame({'peil': x_ax,
                       'score': score,
                       'text': y_hover,
                       'label': pd.cut(score,
                                       bins=bins_bar,
                                       labels=colors_bar.keys())
                       })
    print(df)
    for label, label_df in df.groupby('peil'):
        print(label)
        print(label_df)
        a_fig.add_trace(
            go.Bar(
                x=label_df.peil,
                y=label_df.score,
                hoverinfo="text",
                hovertext=label_df.text,
                name=label
            ),
            a_row,
            a_col
        )
    # for label, label_df in df.groupby('label'):
    #     a_fig.add_trace(
    #         go.Bar(
    #             x=label_df.x,
    #             y=label_df.y,
    #             hoverinfo="text",
    #             hovertext=label_df.text,
    #             name=label,
    #             marker={'color': colors_bar[label]}
    #         ),
    #         a_row,
    #         a_col
    #     )
    a_fig.update_yaxes(
        showticklabels=False,
        range=[0, 4.5],
        row=a_row,
        col=a_col
    )

def plot_voortgang(a_row, a_col, a_fig, a_peil):
    # plotting de gauge
    plot_bgcolor = "#fff"
    quadrant_colors = list(colors_bar.values())[1:]
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


def plot_student(course_config, a_student):
    specs = [[{'type': 'scatter', 'colspan': 2}, None, {'type': 'scatter', 'colspan': 2}, None],
             [{'type': 'scatter', "colspan": 2}, None, {'type': 'bar'}, {'type': 'domain'}]]
    titles = ["Team", "Kennis", "Gilde", "Perspectief", "Voortgang"] #, "Peilmomenten"
    positions = {'team': {'row': 1, 'col': 1}, 'gilde': {'row': 2, 'col': 1}, 'kennis': {'row': 1, 'col': 3}, 'peil': {'row': 2, 'col': 4}}
    fig = make_subplots(rows=2, cols=4, subplot_titles=titles, specs=specs, vertical_spacing=0.15, horizontal_spacing=0.08)
    for perspective in a_student.perspectives:
        row = positions[perspective.name]['row']
        col = positions[perspective.name]['col']
        if perspective.name == "peil":
            plot_peilmoment_bar(2, 3, fig, perspective)
            # Voortgang overall
            if a_student.get_peilmoment(247774):
                plot_voortgang(row, col, fig, a_student.get_peilmoment(247774).score + 0.5)
            else:
                plot_voortgang(row, col, fig, 0.1)
        else:
            assigment_group = course_config.find_assignment_group(perspective.assignment_groups[0])
            plot_bandbreedte(row, col, fig, assigment_group)
            plot_submissions(row, col, fig, perspective.submissions)

    fig.update_layout(height=800, width=1200, showlegend=False)
    fig.update_xaxes(title_text="Dagen in semester", range=[0, days_in_semester], row=1, col=1)
    fig.update_xaxes(title_text="Dagen in semester", range=[0, days_in_semester], row=2, col=1)
    fig.update_xaxes(title_text="Dagen in semester", range=[0, days_in_semester], row=1, col=3)
    file_name = plot_path + student.name + ".html"
    asci_file_name = file_name.translate(translation_table)
    print(asci_file_name)
    fig.write_html(asci_file_name, include_plotlyjs="cdn")


count = 0
for group in results.studentGroups:
    for student in group.students:
        count += 1
        if count == 30:
            plot_student(course, student)


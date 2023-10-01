import math
import kaleido
import textwrap
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

from lib.build_plotly_perspective import plot_perspective, plot_progress, find_submissions
from lib.config import plot_path, date_to_day, peil_labels, hover_style, get_marker_size, score_dict, fraction_to_level, \
    colors_bar, get_date_time_loc
from lib.file import read_start, read_course, read_results
from lib.translation_table import translation_table
from lib_peil import get_bar_score

traces = []
start = read_start()
g_course = read_course(start.course_file_name)
g_results = read_results(start.results_file_name)

g_days_in_semester = (start.end_date - start.start_date).days
print("days_in_semester", g_days_in_semester)
g_actual_day = (g_results.actual_date - start.start_date).days
g_start_date = start.start_date


bins_bar = [0, 0.9, 1.9, 2.9, 3.9, 4.9]
# Define bar properties
specs = [
            [
                {'type': 'scatter', 'colspan': 3, "rowspan": 2}, None, None, {'type': 'scatter', 'colspan': 3, "rowspan": 2}, None, None
            ],
            [
                None, None, None, None, None, None,
            ],
            [
                {'type': 'scatter', "colspan": 3, "rowspan": 2}, None, None, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}
            ],
            [
                None, None, None, None, None, None,
            ]
]

titles = ["Team", "Kennis", "Gilde", "Halfweg", "Ná sprint 7", "Beoordeling"]
positions = {'team': {'row': 1, 'col': 1},
             'gilde': {'row': 3, 'col': 1},
             'kennis': {'row': 1, 'col': 4},
             'halfweg': {'row': 3, 'col': 4},
             'eind': {'row': 3, 'col': 5},
             'beoordeling': {'row': 3, 'col': 6}}


def peil_contruct(a_course):
    peilingen = {}
    for peil in peil_labels:
        peilingen[peil] = []
    peil_perspective = a_course.find_perspective_by_name(start.peil_perspective)
    assignment_group = a_course.find_assignment_group(peil_perspective.assignment_groups[0])
    for assignment in assignment_group.assignments:
        for peil_label in peil_labels:
            if peil_label.lower() in assignment.name.lower():
                peilingen[peil_label].append(assignment)
    return peilingen


def peil_contruct_new(a_course):
    l_peilingen = {}
    for perspective in a_course.perspectives:
        # peil is niet echt een perspective
        if perspective.name != 'peil':
            l_peilingen[perspective.name] = []
    peil_perspective = a_course.find_perspective_by_name(start.peil_perspective)
    print(peil_perspective)
    assignment_group = a_course.find_assignment_group(peil_perspective.assignment_groups[0])
    for assignment in assignment_group.assignments:
        #zoek de juiste Assignment
        for peil_label in peil_labels:
            if peil_label.lower() in assignment.name.lower():
                #zoek het juiste Perspective
                for perspective_name in l_peilingen:
                    if perspective_name.lower() in assignment.name.lower():
                        l_peilingen[perspective_name].append({'assignment': assignment, 'submission': None})
    return l_peilingen


# zoek het juiste peilmoment
def get_bar_perspective(a_course, a_peilmoment):
    # "peil"
    peil_perspective = a_course.find_perspective_by_name(start.peil_perspective)
    for perspective in a_course.perspectives:

        if perspective.name != peil_perspective.name:
            if perspective.name.lower() in a_peilmoment.name.lower():
                return perspective.name
    return None


def get_bar_hover(a_peilmoment):
    score = 0.1
    hover = "Geen data"
    if a_peilmoment:
        if a_peilmoment.graded:
            score = a_peilmoment.score + 1
        if "Beoordeling" in a_peilmoment.assignment_name:
            hover = a_peilmoment.assignment_name + " - " + score_dict[int(score - 1)]['beoordeling']
        else:
            hover = a_peilmoment.assignment_name + " - " + score_dict[int(score-1)]["voortgang"]
        for comment in a_peilmoment.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
    return hover


def plot_voortgang(a_row, a_col, a_fig, a_course, a_perspective):
    score = []
    x_ax = []
    y_hover = []
    perspective = []

    # make data structure
    for peil in peil_construction:
        for assignment in peil_construction[peil]:
            perspective_str = get_bar_perspective(a_course, assignment)
            if perspective_str:
                submission = a_perspective.get_submission_by_assignment(assignment.id)
                x_ax.append(peil)
                score.append(get_bar_score(submission))
                perspective.append(perspective_str)
                if submission:
                    y_hover.append(get_bar_hover(submission))
                    l_row = positions[perspective_str]['row']
                    l_col = positions[perspective_str]['col']
                    l_day = date_to_day(start.start_date, submission.submitted_at)
                    a_fig.add_trace(
                        go.Scatter(
                            x=[l_day],
                            y=[0],
                            hoverinfo="text",
                            hovertext=[get_bar_hover(submission)],
                            mode='markers',
                            marker_color=score_dict[int(submission.score)]['color'],
                            hoverlabel=hover_style,
                            marker=dict(
                                size=20,
                                symbol="arrow-down"
                            )
                        ),
                        row=l_row, col=l_col
                    )
                else:
                    y_hover.append(assignment.name+" - geen data")


    # print(x_ax)
    # print(perspective)
    # print(score)
    df = pd.DataFrame({'peil': x_ax,
                       'perspective': perspective,
                       'score': score,
                       'text': y_hover,
                       'label': pd.cut(score,
                                       bins=bins_bar,
                                       labels=colors_bar.keys())
                       })
    # print("== ", df.loc[:, ['peil', 'perspective', 'score', 'label']] )
    index = 0
    for peil_label in peil_labels:
        index += 1
        for label, label_df in df.loc[df['peil'] == peil_label].groupby('label'):

            # print("peil_label", peil_label)
            # print("label", label)
            # print("label_df", label_df.text)
            a_fig.add_trace(
                go.Bar(
                    x=label_df.perspective,
                    y=label_df.score,
                    hoverinfo="text",
                    hovertext=label_df.text,
                    name="perspective",
                    hoverlabel=hover_style,
                    offsetgroup=index,
                    marker={'color': colors_bar[label]}
                ),
                a_row,
                a_col
            )

    a_fig.update_layout(barmode='group')
    a_fig.update_yaxes(
        showticklabels=False,
        range=[0, 4.5],
        row=a_row,
        col=a_col
    )

def plot_gauge(a_row, a_col, a_fig, a_peil):
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


def plot_student(a_course, a_student, a_peil_construction):
    fig = make_subplots(rows=4, cols=6, subplot_titles=titles, specs=specs, vertical_spacing=0.15, horizontal_spacing=0.08)
    fig.update_layout(height=1000, width=1200, showlegend=False)
    for perspective in a_student.perspectives:
        if perspective.name in a_peil_construction:
            row = positions[perspective.name]['row']
            col = positions[perspective.name]['col']
            plot_progress(row, col, fig, a_peil_construction[perspective.name], start.start_date)
            assigment_group = a_course.find_assignment_group(perspective.assignment_groups[0])
            plot_perspective(row, col, fig, assigment_group, perspective, g_start_date, g_actual_day, g_days_in_semester, get_date_time_loc(g_results.actual_date))

    if a_student.get_peilmoment(247774):
        plot_gauge(positions['halfweg']['row'], positions['halfweg']['col'], fig,
                   a_student.get_peilmoment(247774).score + 0.5)
    else:
        plot_gauge(positions['halfweg']['row'], positions['halfweg']['col'], fig, 0.1)

    if a_student.get_peilmoment(252847):
        plot_gauge(positions['eind']['row'], positions['eind']['col'], fig,
                   a_student.get_peilmoment(252847).score + 0.5)
    else:
        plot_gauge(positions['eind']['row'], positions['eind']['col'], fig, 0.1)

    if a_student.get_peilmoment(253129):
        plot_gauge(positions['beoordeling']['row'], positions['beoordeling']['col'], fig,
                   a_student.get_peilmoment(253129).score + 0.5)
    else:
        plot_gauge(positions['beoordeling']['row'], positions['beoordeling']['col'], fig, 0.1)
    file_name = plot_path + a_student.name
    asci_file_name = file_name.translate(translation_table)
    fig.write_html(asci_file_name+ ".html", include_plotlyjs="cdn")
    fig.write_image(asci_file_name+ ".jpeg")
    volg_nr = str(g_actual_day).zfill(3)
    file_name = "./time_lap/" + a_student.name + "_" + volg_nr + ".jpeg"
    asci_file_name = file_name.translate(translation_table)
    fig.write_image(asci_file_name)


peil_construction = peil_contruct_new(g_course)
# for perspective in peil_construction:
#     print(perspective)
#     for assignment in peil_construction[perspective]:
#         print(assignment)

count = 0
for student in g_results.students:
    l_peil_construction = find_submissions(student, peil_construction.copy())
    print(student.name)
    plot_student(g_course, student, l_peil_construction)


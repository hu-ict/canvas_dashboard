import math
import textwrap
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from lib.config import plot_path, voortgang_tabel, date_to_day, peil_labels, colors_bar, hover_style, score_tabel, \
    color_tabel, get_marker_size, beoordeling_tabel
from lib.file import read_start, read_course, read_results
from lib.translation_table import translation_table

traces = []
start = read_start()
g_course = read_course(start.course_file_name)
results = read_results(start.results_file_name)

days_in_semester = (start.end_date - start.start_date).days
print("days_in_semester", days_in_semester)
actual_day = (results.actual_date - start.start_date).days
bins_bar = [0, 0.9, 1.9, 2.9, 3.9, 4.9]
# Define bar properties
specs = [[{'type': 'scatter', 'colspan': 2, "rowspan": 2}, None, {'type': 'scatter', 'colspan': 2, "rowspan": 2}, None],
         [None, None, None, None],
         [{'type': 'scatter', "colspan": 2, "rowspan": 2}, None, {'type': 'domain'}, {'type': 'bar'}],
         [None, None, {'type': 'domain'}, {'type': 'domain'}]]
titles = ["Team", "Kennis", "Gilde", "Halfweg", "Peilmoment", "Ná sprint 7", "Beoordeling"]
positions = {'team': {'row': 1, 'col': 1}, 'gilde': {'row': 3, 'col': 1}, 'kennis': {'row': 1, 'col': 3},
             'peil': {'row': 3, 'col': 4}, 'halfweg': {'row': 3, 'col': 3}, 'eind': {'row': 4, 'col': 3},
             'beoordeling': {'row': 4, 'col': 4}}

print(colors_bar.keys())


def calc_dev(iterations, r, a, b, c):
    iteration_list = []
    for x in range(iterations-r):
        y = a*x*x+b*x+c
        if y < 0:
            y = 0
        iteration_list.append(y)
    for x in range(r):
        iteration_list.append(y)
    return iteration_list


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


def plot_bandbreedte(a_row, a_col, a_fig, assignment_group):
    if assignment_group.total_points <= 0:
        return
    x_time = calc_dev(days_in_semester, 0, 0, 1, 0)
    # bereken bandbreedte
    if assignment_group.name == "TEAM":
        band_lower = calc_dev(days_in_semester, 14, 0.0012, 0.05, -1)
        band_upper = calc_dev(days_in_semester, 14, 0.001786, 0.05, 6)
    else:
        b = assignment_group.lower_points / (days_in_semester-14 - 30)
        c = - 30 * b
        band_lower = calc_dev(days_in_semester, 14, 0, b, c)
        band_upper = calc_dev(days_in_semester, 14, 0, b, c + assignment_group.upper_points - assignment_group.lower_points)

    a_fig.add_trace(
        go.Scatter(
            x=[actual_day,actual_day+2,actual_day+2,actual_day,actual_day],
            y=[0,0,20,20,0],
            fill="toself",
            mode='lines',
            name='',
            hoverlabel=hover_style,
            text='Dag van snapshot in semester',
            opacity=0
        ),
        row=a_row, col=a_col
    )
    a_fig.add_shape(
        dict(type="rect", x0=actual_day, x1=actual_day+1, y0=0, y1=200,
             fillcolor="#888888", line_color="#888888"
             ),
        row=a_row,
        col=a_col
    )

    a_fig.update_yaxes(title_text="Punten", range=[0, assignment_group.total_points], row=a_row, col=a_col)

    # teken bandbreedte
    a_fig.add_trace(
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


def plot_submissions(a_row, a_col, a_fig, a_perspective):
    x_submission = [0]
    y_submission = [0]
    y_hover = ['Start']
    y_colors = [color_tabel[0]]
    y_size = [get_marker_size(False)]
    cum_score = 0
    l_submissions = sorted(a_perspective.submissions, key=lambda s: s.submitted_at)
    for submission in l_submissions:
        y_size.append(get_marker_size(submission.graded))
        x_submission.append(date_to_day(start.start_date, submission.submitted_at))
        cum_score += submission.score
        y_submission.append(cum_score)
        if 0 <= submission.score <= 3:
            y_colors.append(color_tabel[int(submission.score)])
        else:
            y_colors.append(color_tabel[4])
        if a_perspective.name == "kennis":
            hover = submission.assignment_name + "<br>Score: " + str(submission.score)
        else:
            hover = submission.assignment_name + "<br>" + score_tabel[int(submission.score)]
        for comment in submission.comments:
            value = comment.author_name + " - " + comment.comment
            wrapper = textwrap.TextWrapper(width=75)
            word_list = wrapper.wrap(text=value)
            for line in word_list:
                hover += "<br>" + line
        y_hover.append(hover)

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
    a_fig.update_xaxes(title_text="Dagen in semester", range=[0, days_in_semester], row=a_row, col=a_col)
    return {"x": x_submission, "y": y_submission}


# zoek het juiste peilmoment
def get_bar_perspective(a_course, a_peilmoment):
    # "peil"
    peil_perspective = a_course.find_perspective_by_name(start.peil_perspective)
    for perspective in a_course.perspectives:

        if perspective.name != peil_perspective.name:
            if perspective.name.lower() in a_peilmoment.name.lower():
                return perspective.name
    return None


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
        if "Beoordeling" in a_peilmoment.assignment_name:
            hover = a_peilmoment.assignment_name + " - " + beoordeling_tabel[int(score - 1)]
        else:
            hover = a_peilmoment.assignment_name + " - " + voortgang_tabel[int(score-1)]
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
                            marker_color=color_tabel[int(submission.score)],
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


def plot_student(a_course, a_student):
    fig = make_subplots(rows=4, cols=4, subplot_titles=titles, specs=specs, vertical_spacing=0.15, horizontal_spacing=0.08)
    fig.update_layout(height=1000, width=1200, showlegend=False)
    for perspective in a_student.perspectives:
        row = positions[perspective.name]['row']
        col = positions[perspective.name]['col']
        if perspective.name == start.peil_perspective:
            plot_voortgang(row, col, fig, a_course, perspective)
            # Voortgang overall
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
        else:
            assigment_group = a_course.find_assignment_group(perspective.assignment_groups[0])
            plot_bandbreedte(row, col, fig, assigment_group)
            plot_submissions(row, col, fig, perspective)

    file_name = plot_path + a_student.name + ".html"
    asci_file_name = file_name.translate(translation_table)
    print(asci_file_name)
    fig.write_html(asci_file_name, include_plotlyjs="cdn")


peil_construction = peil_contruct(g_course)
# for peil in peil_construction.values():
#     for assignment in peil:
#         print(assignment)

count = 0
for group in results.student_groups:
    for student in group.students:
        plot_student(g_course, student)


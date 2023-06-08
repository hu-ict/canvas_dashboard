import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from lib.config import peil_labels, voortgang_tabel, color_tabel, hover_style, plot_path

def plot_totals(course_config_start, course, student_totals):
    titles = ["Team", "Gilde", 'Kennis', 'Team', 'Gilde', 'Kennis', 'Halfweg', 'Eind', 'Beoordeling', 'Vertraging']
    specs = [
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
        [{'type': 'bar'}, None, None]
    ]

    fig = make_subplots(rows=4, cols=3, specs=specs, subplot_titles=titles)
    fig.update_layout(height=1400, width=1200, showlegend=False)
    data = go.Histogram(x=np.array(student_totals['team']['count']))
    fig.add_trace(data, 1, 1)
    data = go.Histogram(x=np.array(student_totals['gilde']['count']), marker=dict(color="#f6c23e"))
    fig.add_trace(data, 1, 2)
    data = go.Histogram(x=np.array(student_totals['kennis']['count']))
    fig.add_trace(data, 1, 3)

    fig.update_xaxes(title_text="Punten")

    fig.update_layout(
        title_text='Scores studenten',  # title of plot
        xaxis_title_text='Punten',  # xaxis label
        xaxis2_title_text='Punten',  # xaxis label
        xaxis3_title_text='Percentage',  # xaxis label
        xaxis4_title_text='Pending',  # xaxis label
        xaxis5_title_text='Pending',  # xaxis label
        xaxis6_title_text='Pending',  # xaxis label
        xaxis7_title_text='Dagen na inlevering',  # xaxis label
        yaxis_title_text='Aantal',  # yaxis label
        yaxis4_title_text='Aantal',  # yaxis label
        # yaxis9_title_text='Aantal',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # gap between bars of the same location coordinates
        barmode='stack'
    )

    col = 0
    for l_perspective in course.perspectives:
        if l_perspective.name != course_config_start.peil_perspective:
            col += 1
            x_team = list(student_totals[l_perspective.name]['pending'].keys())
            y_counts = list(student_totals[l_perspective.name]['pending'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Pending", marker=dict(color="#4e73df")), 2, col)
            x_team = list(student_totals[l_perspective.name]['late'].keys())
            y_counts = list(student_totals[l_perspective.name]['late'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Late", marker=dict(color="#e74a3b")), 2, col)
            x_team = list(student_totals[l_perspective.name]['to_late'].keys())
            y_counts = list(student_totals[l_perspective.name]['to_late'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="To Late", marker=dict(color="#555555")), 2, col)

    data = go.Histogram(x=np.array(student_totals['late']['count']))
    fig.add_trace(data, 4, 1)

    col = 0
    for peil_label in peil_labels:
        col += 1
        values = []
        labels = []
        colors = [color_tabel[0]]
        for value in student_totals['peil'][peil_label].values():
            values.append(value)
        for key in student_totals['peil'][peil_label].keys():
            labels.append(voortgang_tabel[key])
        for color in color_tabel.values():
            colors.append(color)
        # print(labels)
        # print(values)
        # print(colors)
        trace = go.Pie(
            values=values,
            labels=labels, marker_colors=colors,
            direction='clockwise',
            sort=False, hoverlabel=hover_style)
        # data = [trace]
        # fig = go.Figure(data=data)

        fig.add_trace(
            trace,
            3, col)
        fig.update_yaxes(title_text="Aantal", range=[0, 40], row=2, col=col)

    file_name = plot_path + "totals" + ".html"
    fig.write_html(file_name, include_plotlyjs="cdn")


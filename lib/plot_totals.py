import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from lib.config import peil_labels, voortgang_tabel, color_tabel, hover_style, plot_path, beoordeling_tabel, peil_levels
import numpy as np

def plot_peilingen(a_fig, course_config_start, course, student_totals):
# Create dummy data indexed by month and with multi-columns [product, revenue]
    index = ["Overall"]
    color_tabel = {
        -1: '#aaaaaa',
        0: '#f25829',
        1: '#f2a529',
        2: '#85e043',
        3: '#2bad4e'
    }
    l_perspective = "overall"

    for level in peil_levels:
        y_counts = []
        x_labels = []
        y_hover = []
        for label in peil_labels:
            x_labels.append(label)
            y_counts.append(student_totals['peil'][label][l_perspective][level])
            y_hover.append(label+" "+voortgang_tabel[level]+" "+str(student_totals['peil'][label][l_perspective][level]))
        a_fig.add_trace(go.Bar(x=x_labels, y=y_counts,
                               name=voortgang_tabel[level],
                               hoverinfo="text",
                               hovertext=y_hover,
                               hoverlabel=hover_style,
                               text=y_counts,
                               marker=dict(color=color_tabel[level])), 3, 1)

    a_fig.update_yaxes(title_text="Aantal", range=[0, 150], row=3, col=1)


def plot_totals(course_config_start, course, student_totals):
    titles = ["Team", "Gilde", 'Kennis',
              'Team', 'Gilde', 'Kennis',
              'Overall', 'Vertraging']
    specs = [
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'domain'}]
    ]

    fig = make_subplots(rows=3, cols=3, specs=specs, subplot_titles=titles)
    fig.update_layout(height=1200, width=1200, showlegend=False)
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
        xaxis7_title_text='Peilmomenten',  # xaxis label
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
    fig.add_trace(data, 3, 2)
    plot_peilingen(fig, course_config_start, course, student_totals)
    file_name = plot_path + "totals" + ".html"
    fig.write_html(file_name, include_plotlyjs="cdn")


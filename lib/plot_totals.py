import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

from lib.lib_plotly import peil_levels, score_dict, hover_style, peil_labels, plot_path


def plot_actuals(a_fig, a_progress_history):
    for level in peil_levels:
        y_counts = []
        x_labels = []
        y_hover = []
        for day in a_progress_history.days:
            x_labels.append(day.day)
            y_counts.append(day.progress[str(level)])
            y_hover.append("Dag: "+str(day.day) + ", " + score_dict['voortgang'][level]['niveau'] + ", aantal: " + str(day.progress[str(level)]))
        a_fig.add_trace(go.Bar(x=x_labels, y=y_counts,
                               name=score_dict['voortgang'][level]['niveau'],
                               hoverinfo="text",
                               hovertext=y_hover,
                               hoverlabel=hover_style,
                               text=y_counts,
                               marker=dict(color=score_dict['voortgang'][level]['color'])), 2, 2)
    a_fig.update_yaxes(title_text="Aantal", range=[0, 100], row=2, col=2)

def plot_peilingen(a_fig, student_totals):
    l_perspective = "overall"
    for level in peil_levels:
        y_counts = []
        x_labels = []
        y_hover = []
        for label in peil_labels:
            x_labels.append(label)
            y_counts.append(student_totals['peil'][label][l_perspective][level])
            y_hover.append(label+" "+score_dict['voortgang'][level]['niveau']+" "+str(student_totals['peil'][label][l_perspective][level]))
        a_fig.add_trace(go.Bar(x=x_labels, y=y_counts,
                               name=score_dict['voortgang'][level]['niveau'],
                               hoverinfo="text",
                               hovertext=y_hover,
                               hoverlabel=hover_style,
                               text=y_counts,
                               marker=dict(color=score_dict['voortgang'][level]['color'])), 2, 1)

    a_fig.update_yaxes(title_text="Aantal", range=[0, 100], row=2, col=1)


def plot_totals(course_config_start, course, student_totals, progress_history):
    titles = ['Team', 'Gilde','Kennis',
              'Overall', 'Dagelijkse voortgang', 'Vertraging']
    specs = [
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]
    ]

    fig = make_subplots(rows=2, cols=3, specs=specs, subplot_titles=titles)
    fig.update_layout(height=900, width=1200, showlegend=False)
    fig.update_layout(
        title_text='Reviews',  # title of plot
        xaxis_title_text='Pending',  # xaxis label
        xaxis2_title_text='Pending',  # xaxis label
        xaxis3_title_text='Pending',  # xaxis label
        xaxis4_title_text='Peilmomenten',  # xaxis label
        xaxis5_title_text='Dag',  # xaxis label
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
            x_team = list(student_totals['perspectives'][l_perspective.name]['pending'].keys())
            y_counts = list(student_totals['perspectives'][l_perspective.name]['pending'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Pending", marker=dict(color="#4e73df")), 1, col)
            x_team = list(student_totals['perspectives'][l_perspective.name]['late'].keys())
            y_counts = list(student_totals['perspectives'][l_perspective.name]['late'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Late", marker=dict(color="#e74a3b")), 1, col)
            x_team = list(student_totals['perspectives'][l_perspective.name]['to_late'].keys())
            y_counts = list(student_totals['perspectives'][l_perspective.name]['to_late'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="To Late", marker=dict(color="#555555")), 1, col)

    data = go.Histogram(x=np.array(student_totals['late']['count']))
    fig.add_trace(data, 2, 3)
    plot_peilingen(fig, student_totals)
    plot_actuals(fig, progress_history)
    file_name = plot_path + "totals" + ".html"
    fig.write_html(file_name, include_plotlyjs="cdn")


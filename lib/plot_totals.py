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


def plot_gilde(a_fig, a_totals):
    colors = {
        'CSC_C': '#e74a3b',
        'TI': '#36b9cc',
        'BIM': '#1cc88a',
        'SD_B': '#5a5c69'
    }
    for role in a_totals:
        y_counts = []
        x_labels = []
        y_hover = []
        for key in a_totals[role]:
            x_labels.append(key)
            y_counts.append(a_totals[role][key])
            y_hover.append("Gilde: " + role + " " + str(key) + " punten,  "+str(a_totals[role][key]) + "%")
        a_fig.add_trace(go.Scatter(x=x_labels, y=y_counts,
                               hovertext=y_hover,
                               hoverlabel=hover_style,
                                mode='lines+markers',
                                marker_color=colors[role],
                                line_color=colors[role],
                               offsetgroup=key,
                               text=y_counts), 3, 1)
    a_fig.update_yaxes(title_text="Percentage", range=[0, 80], row=3, col=1)
    a_fig.update_xaxes(title_text="Punten", range=[0, 9], row=3, col=1)


def plot_team(a_fig, a_totals):
    colors = {
        'DD': '#e74a3b',
        'BW': '#36b9cc',
        'HVG': '#1cc88a',
        'KE': '#f6c23e',
        'RH': '#5a5c69'
    }
    for role in a_totals:
        y_counts = []
        x_labels = []
        y_hover = []
        for key in a_totals[role]:
            x_labels.append(key)
            y_counts.append(a_totals[role][key])
            y_hover.append("Team: " + role + " " + str(key) + " punten,  " + str(a_totals[role][key]) + "%")
        a_fig.add_trace(go.Scatter(x=x_labels, y=y_counts,
                                   hovertext=y_hover,
                                   hoverlabel=hover_style,
                                   mode='lines+markers',
                                   marker_color=colors[role],
                                   line_color=colors[role],
                                   offsetgroup=key,
                                   text=y_counts), 3, 2)
    a_fig.update_yaxes(title_text="Percentage", range=[0, 80], row=3, col=2)
    a_fig.update_xaxes(title_text="Punten", range=[0, 9], row=3, col=2)


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



def plot_totals(course_config_start, course, student_totals, progress_history, gilde, team):
    titles = ['Team', 'Gilde','Kennis',
              'Overall', 'Dagelijkse voortgang', 'Vertraging',
              'Gilde', 'Team', ''
              ]
    specs = [
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'scatter'}, {'type': 'scatter'}, {'type': 'bar'}]
    ]

    fig = make_subplots(rows=3, cols=3, specs=specs, subplot_titles=titles)
    fig.update_layout(height=1200, width=1200, showlegend=False)
    fig.update_layout(
        title_text='Reviews',  # title of plot
        xaxis_title_text='Pending',  # xaxis perspective
        xaxis2_title_text='Pending',  # xaxis perspective
        xaxis3_title_text='Pending',  # xaxis perspective
        xaxis4_title_text='Peilmomenten',  # xaxis perspective
        xaxis5_title_text='Dag',  # xaxis perspective
        yaxis_title_text='Aantal',  # yaxis perspective
        yaxis4_title_text='Aantal',  # yaxis perspective
        # yaxis9_title_text='Aantal',  # yaxis perspective
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # gap between bars of the same location coordinates
        barmode='stack'
    )

    col = 0
    for l_perspective in course.perspectives.perspectives:
        if l_perspective != course_config_start.peil_perspective:
            col += 1
            x_team = list(student_totals['perspectives'][l_perspective]['pending'].keys())
            y_counts = list(student_totals['perspectives'][l_perspective]['pending'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Pending", marker=dict(color="#4e73df")), 1, col)
            x_team = list(student_totals['perspectives'][l_perspective]['late'].keys())
            y_counts = list(student_totals['perspectives'][l_perspective]['late'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Late", marker=dict(color="#e74a3b")), 1, col)
            x_team = list(student_totals['perspectives'][l_perspective]['to_late'].keys())
            y_counts = list(student_totals['perspectives'][l_perspective]['to_late'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="To Late", marker=dict(color="#555555")), 1, col)

    data = go.Histogram(x=np.array(student_totals['late']['count']))
    fig.add_trace(data, 2, 3)
    plot_peilingen(fig, student_totals)
    plot_actuals(fig, progress_history)
    plot_gilde(fig, gilde)
    plot_team(fig, team)
    file_name = plot_path + "totals" + ".html"
    fig.write_html(file_name, include_plotlyjs="cdn")


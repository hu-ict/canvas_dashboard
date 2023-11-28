import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from lib.lib_plotly import peil_levels, hover_style, peil_labels


def plot_progress_history(a_fig, a_row, a_col, a_progress_history, a_start, a_course, a_labels_colors):
    x = []
    for day in a_progress_history.days:
        x.append(day.day)

    for level in peil_levels:
        y = []
        y_hover = []
        l_label = a_labels_colors.level_series[a_start.progress_levels].levels[str(level)].label
        l_color = a_labels_colors.level_series[a_start.progress_levels].levels[str(level)].color
        for day in a_progress_history.days:
            y.append(day.progress[str(level)])
            y_hover.append("Dag: "+str(day.day) + ", " + l_label + ", aantal: " + str(day.progress[str(level)]))
        # print(level)
        # print(x)
        # print(y)
        a_fig.add_trace(go.Scatter(
            x=x, y=y,
            fillcolor=l_color,
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines',
            line=dict(width=2, color=l_color),
            stackgroup='one'  # define stack group
        ), a_row, a_col)
    y_axis = len(a_course.students)
    a_fig.update_yaxes(title_text="Aantal", range=[0, y_axis], row=a_row, col=a_col)


def plot_actuals(a_fig, a_row, a_col, a_progress_history, a_course, a_labels_colors):
    for level in peil_levels:
        y_counts = []
        x_labels = []
        y_hover = []
        for day in a_progress_history.days:
            x_labels.append(day.day)
            y_counts.append(day.progress[str(level)])
            l_label = a_labels_colors.level_series[a_course.perspectives[a_course.progress_perspective].levels].levels[str(level)].label
            l_color = a_labels_colors.level_series[a_course.perspectives[a_course.progress_perspective].levels].levels[str(level)].color
            y_hover.append("Dag: "+str(day.day) + ", " + l_label + ", aantal: " + str(day.progress[str(level)]))
        a_fig.add_trace(go.Bar(x=x_labels, y=y_counts,
                               name=l_label,
                               hoverinfo="text",
                               hovertext=y_hover,
                               hoverlabel=hover_style,
                               text=y_counts,
                               marker=dict(color=l_color)), a_row, a_col)
    y_axis = len(a_course.students)
    a_fig.update_yaxes(title_text="Aantal", range=[0, y_axis], row=a_row, col=a_col)


def plot_gilde(a_fig, a_row, a_col, a_totals):
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


def plot_team(a_fig, a_row, a_col, a_totals):
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
            y_hover.append("Team: " + str(role) + " " + str(key) + " punten,  " + str(a_totals[role][key]) + "%")
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


def plot_peilingen(a_fig, a_row, a_col, student_totals, a_start, a_course, a_labels_colors):
    l_perspective = "overall"
    for level in peil_levels:
        y_counts = []
        x_labels = []
        y_hover = []
        for label in peil_labels:
            x_labels.append(label)
            y_counts.append(student_totals[a_start.progress_perspective][label][l_perspective][level])
            y_hover.append(label+" "+a_labels_colors.level_series[a_start.progress_levels].levels[str(level)].label+" "+str(student_totals[a_start.progress_perspective][label][l_perspective][level]))
        a_fig.add_trace(go.Bar(x=x_labels, y=y_counts,
                               name=a_labels_colors.level_series[a_start.progress_levels].levels[str(level)].label,
                               hoverinfo="text",
                               hovertext=y_hover,
                               hoverlabel=hover_style,
                               text=y_counts,
                               marker=dict(color=a_labels_colors.level_series[a_start.progress_levels].levels[str(level)].color)), row=a_row, col=a_col)
    y_axis = len(a_course.students)
    a_fig.update_yaxes(title_text="Aantal", range=[0, y_axis], row=a_row, col=a_col)


def plot_totals(a_instances, start, course, student_totals, progress_history, a_labels_colors):
    if a_instances.is_instance_of("inno_courses"):
        titles = ['Team', 'Gilde','Kennis',
                  'Dagelijkse voortgang', 'Voortgang overall', 'Vertraging']
    else:
        titles = ['Project', 'Finals', 'Toets',
                  'Dagelijkse voortgang', '', 'Vertraging']

    specs = [
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]
    ]
    fig = make_subplots(rows=2, cols=3, specs=specs, subplot_titles=titles)
    fig.update_layout(
        title_text='Reviews',  # title of plot
        xaxis_title_text='Pending',  # xaxis perspective
        xaxis2_title_text='Pending',  # xaxis perspective
        xaxis3_title_text='Pending',  # xaxis perspective
        yaxis_title_text='Aantal',  # yaxis perspective
        yaxis4_title_text='Aantal',  # yaxis perspective
        # yaxis9_title_text='Aantal',  # yaxis perspective
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # gap between bars of the same location coordinates
        barmode='stack'
    )
    fig.update_layout(height=800, width=1200, showlegend=False)

    col = 0
    for l_perspective in course.perspectives:
        if l_perspective != start.progress_perspective and l_perspective != "aanwezig":
            print(l_perspective)
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

    plot_progress_history(fig, 2, 1, progress_history, start, course, a_labels_colors)
    data = go.Histogram(x=np.array(student_totals['late']['count']))
    fig.add_trace(data, 2, 3)
    if start.progress_perspective:
        plot_peilingen(fig, 2, 2, student_totals, start, course, a_labels_colors)

    file_name = a_instances.get_plot_path() + "totals" + ".html"
    fig.write_html(file_name, include_plotlyjs="cdn")


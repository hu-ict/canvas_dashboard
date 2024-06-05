import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
from lib.lib_plotly import hover_style


def plot_progress_history(a_fig, a_row, a_col, a_progress_history, a_perspective_name, a_course, a_progress_levels):
    x = []
    for day in a_progress_history.days:
        x.append(day.day)

    for level in a_progress_levels.levels.keys():
        y = []
        y_hover = []
        l_label = a_progress_levels.levels[str(level)].label
        l_color = a_progress_levels.levels[str(level)].color
        for day in a_progress_history.days:
            if a_perspective_name == "overall":
                y.append(day.progress[str(level)])
                y_hover.append("Dag: "+str(day.day) + ", " + l_label + ", aantal: " + str(day.progress[str(level)]))
            else:
                y.append(day.perspective[a_perspective_name][str(level)])
                y_hover.append("Dag: "+str(day.day) + ", " + l_label + ", aantal: " + str(day.perspective[a_perspective_name][str(level)]))

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


def plot_workload_history(a_fig, a_row, a_col, a_workload_history):
    x = []
    for day in a_workload_history.days:
        x.append(day.day)
    time_color = {
        "week": "#4e73df",
        "over_week": "#e74a3b",
        "over_14": "#555555"
    }
    for aspect in ["over_14", "over_week", "week"]:
        y = []
        y_hover = []
        for day in a_workload_history.days:
            y.append(day.workload[aspect])
            y_hover.append("Dag: " + str(day.day) + ", " + aspect + ", aantal: " + str(day.workload[aspect]))
        a_fig.add_trace(go.Scatter(
            x=x, y=y,
            fillcolor=time_color[aspect],
            hoverinfo="text",
            hovertext=y_hover,
            mode='lines',
            line=dict(width=2, color=time_color[aspect]),
            stackgroup='one'  # define stack group
        ), a_row, a_col)


def plot_peilingen(a_fig, a_row, a_col, student_totals, a_start, a_course, a_progress_levels):
    for level in a_progress_levels.levels.keys():
        y_counts = []
        x_labels = []
        y_hover = []
        for label in a_course.level_moments.moments:
            x_labels.append(label)
            y_counts.append(student_totals[a_start.level_moments.name][label]["overall"][int(level)])
            y_hover.append(label+" "+a_progress_levels.levels[str(level)].label+" "+str(student_totals[a_start.level_moments.name][label]["overall"][int(level)]))
        a_fig.add_trace(go.Bar(x=x_labels, y=y_counts,
                               name=a_progress_levels.levels[level].label,
                               hoverinfo="text",
                               hovertext=y_hover,
                               hoverlabel=hover_style,
                               text=y_counts,
                               marker=dict(color=a_progress_levels.levels[str(level)].color)), row=a_row, col=a_col)
    y_axis = len(a_course.students)
    a_fig.update_yaxes(title_text="Aantal", range=[0, y_axis], row=a_row, col=a_col)


def plot_voortgang(a_instances, a_start, a_course, student_totals, a_progress_history, a_progress_levels):
    if a_instances.is_instance_of("inno_courses"):
        titles = ['Dagelijkse voortgang <b>studenten</b>', 'Peilingen', "", "Team", "Gilde", "Kennis"]
    else:
        titles = ['Dagelijkse voortgang <b>studenten</b>', 'Peilingen', "", "Kennis", "Oriëntatie", "Professional Skill"]
    specs = [
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]
    ]
    fig = make_subplots(rows=2, cols=3, specs=specs, subplot_titles=titles, vertical_spacing=0.15, horizontal_spacing=0.08)
    fig.update_layout(height=700, width=1200, showlegend=False)
    fig.update_layout(
        title_text='Voortgang',  # title of plot
        xaxis_title_text='Dag in semester',  # xaxis perspective
        yaxis_title_text='Aantal',  # yaxis perspective
        # yaxis9_title_text='Aantal',  # yaxis perspective
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # gap between bars of the same location coordinates
        barmode='stack'
    )
    plot_progress_history(fig, 1, 1, a_progress_history, "overall", a_course, a_progress_levels)
    col = 1
    for perspective in a_start.perspectives.keys():
        plot_progress_history(fig, 2, col, a_progress_history, perspective, a_course, a_progress_levels)
        col += 1
        if col > 3:
            break
    if a_instances.is_instance_of("inno_courses_new") or a_instances.is_instance_of("inno_courses"):
        plot_peilingen(fig, 1, 2, student_totals, a_start, a_course, a_progress_levels)
    file_name = a_instances.get_plot_path() + "totals_voortgang" + ".html"
    fig.write_html(file_name, include_plotlyjs="cdn")

def plot_werkvoorraad(a_instances, a_start, a_course, student_totals, a_workload_history):
    specs = [
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'xy'}, {'type': 'bar'}]
    ]
    if a_instances.is_instance_of("inno_courses"):
        titles = ['Team', 'Gilde','Kennis',
                  'Dagelijkse werkvoorraad <b>docenten</b>', 'Vertraging']
    elif a_instances.is_instance_of("prop_courses"):
        titles = ['Kennis', 'Oriëntatie', 'Professional Skills',
                  'Dagelijkse werkvoorraad <b>docenten</b>', 'Vertraging']
    else:
        titles = ['Project', 'Finals', 'Toets',
                  'Dagelijkse werkvoorraad <b>docenten</b>', 'Vertraging']

    fig = make_subplots(rows=2, cols=3, specs=specs, subplot_titles=titles)
    fig.update_layout(height=800, width=1200, showlegend=False)

    fig.update_layout(
        title_text='Werkvoorraad',  # title of plot
        xaxis_title_text='Pending',  # xaxis perspective
        xaxis2_title_text='Pending',  # xaxis perspective
        xaxis3_title_text='Pending',  # xaxis perspective
        yaxis_title_text='Aantal',  # yaxis perspective
        yaxis4_title_text='Aantal',  # yaxis perspective
        xaxis4_title_text='dag in semester',  # xaxis perspective

        # yaxis9_title_text='Aantal',  # yaxis perspective
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # gap between bars of the same location coordinates
        barmode='stack'
    )

    col = 0
    for l_perspective in a_course.perspectives:
        if l_perspective != "aanwezig":
            print("PT01", l_perspective)
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
    plot_workload_history(fig, 2, 1, a_workload_history)
    data = go.Histogram(x=np.array(student_totals['late']['count']))
    fig.add_trace(data, 2, 2)
    file_name = a_instances.get_plot_path() + "totals_werkvoorraad" + ".html"
    fig.write_html(file_name, include_plotlyjs="cdn")
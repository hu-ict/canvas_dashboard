from plotly.subplots import make_subplots
import plotly.graph_objs as go
from lib.build_plotly_generic import plot_bandbreedte_colored
from lib.translation_table import translation_table


def process_analyse(learning_analytics, assignment, level_serie_collection, filename):
    print("BPA10 - Processing", assignment.name)
    positions = {'status': {'row': 1, 'col': 1},
                 'grades': {'row': 1, 'col': 2}
                 }
    specs = [
        [
            {'type': 'bar'},
            {'type': 'bar'}
        ]
    ]
    fig = make_subplots(rows=1, cols=2, specs=specs)

    for status in learning_analytics[str(assignment.id)]["status"]:
        level_serie_name = learning_analytics[str(assignment.id)]['level_serie']
        level_serie = level_serie_collection.level_series[level_serie_name]
        # print("BPA11 - Status", status, level_serie_name, level_serie.status)
        l_color = level_serie.status[str(status)].color
        x = [level_serie.status[str(status)].label]
        y = [learning_analytics[str(assignment.id)]["status"][status]]
        fig.add_trace(
            go.Bar(x=x,
                   y=y,
                   name="Status",
                   marker=dict(
                       color=l_color),
                   text=y),
            1, 1)
    fig.update_xaxes(title_text="Status", row=1, col=1)

    for grade in learning_analytics[str(assignment.id)]["grades"]:
        level_serie_name = learning_analytics[str(assignment.id)]['level_serie']
        level_serie = level_serie_collection.level_series[level_serie_name]
        l_color = level_serie.grades[str(grade)].color
        x = [level_serie.grades[str(grade)].label]
        y = [learning_analytics[str(assignment.id)]["grades"][grade]]

        fig.add_trace(
            go.Bar(x=x,
                   y=y,
                   name="Waarde",
                   marker=dict(
                       color=l_color),
                   text=y),
            1, 2)
    fig.update_xaxes(title_text="Waarde", row=1, col=2)

    fig.update_yaxes(title_text="Aantal")
    fig.update_layout(height=500, width=1200, showlegend=False)
    fig.update_layout(
        title_text='Analyse van ' + assignment.name,  # title of plot
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # gap between bars of the same location coordinates
        barmode='stack'
    )

    fig.write_html(filename, include_plotlyjs="cdn")

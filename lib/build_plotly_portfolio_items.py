import plotly.graph_objects as go

from lib.translation_table import translation_table


def build_portfolio_items(instances, course, student, levels):
    # maak de kolommen
    header_values = ["Portfolio-item"]
    table_values = []
    for learning_outcome in course.learning_outcomes:
        header_values.append(learning_outcome.short)
        table_values.append([])


    column = 0
    for perspective in course.perspectives:
        course.get_assignment_group(perspective)
    for assignment in learning_outcome.assignments:
        column = 0
        table_values[column].append(assignment.name)
        for learning_outcome in course.learning_outcomes:
            column += 1
            table_values[column].append("Hoi")
    for learning_outcome in course.learning_outcomes:
        column += 1

    fig = go.Figure(data=[go.Table(
        header=dict(values=header_values,
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='left'),
        cells=dict(values=[["Berend", "Anita", "Bart", "André"], # 1st column
                           ["Voldaan", "Te laat", 75, 95],
                           [3, 0, 0, 0]], # 3th column
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='left'))
    ])

    fig.update_layout(width=1200, height=1200)
    file_name = instances.get_plot_path() + student.name + " portfolio1"
    asci_file_name = file_name.translate(translation_table)
    fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
    fig.write_image(asci_file_name + ".jpeg")

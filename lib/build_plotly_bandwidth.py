from plotly.subplots import make_subplots
from lib.build_plotly_generic import plot_bandbreedte_colored
from lib.build_plotly_perspective import plot_assignments
from lib.translation_table import translation_table


def process_bandwidth(a_instances, a_course, a_assignment_group, a_labels_colors):
    if a_assignment_group.strategy == "NONE":
        print("TB06 - No strategy defined for", a_assignment_group.id, "in perspective", a_assignment_group.name)
    print("TB07 - Processing", a_assignment_group.name, "strategy", a_assignment_group.strategy)

    # fig = go.Figure()
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])


    # Add figure title
    fig.update_layout(
        title_text="Double Y Axis Example"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="xaxis title")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
    fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)


    fig.update_layout(height=800, width=1200, showlegend=False)
    plot_bandbreedte_colored(0, 0, fig, a_course.days_in_semester, a_assignment_group.bandwidth, False, a_assignment_group.total_points)

    fig.update_layout(title=f"{a_assignment_group.name}, strategy {a_assignment_group.strategy}", showlegend=False)

    fig.update_yaxes(title_text="Punten", range=[0, a_assignment_group.total_points])
    fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester])

    plot_assignments(0, 0, fig, a_course, True, a_assignment_group.assignment_sequences, a_labels_colors)

    file_name = a_instances.get_html_path() + "bandwidth_"+str(a_assignment_group.id)
    asci_file_name = file_name.translate(translation_table)
    fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
    fig.write_image(asci_file_name + ".jpeg")

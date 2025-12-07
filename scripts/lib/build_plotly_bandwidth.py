from plotly.subplots import make_subplots
from lib.build_plotly_generic import plot_bandbreedte_colored
from lib.build_plotly_perspective import plot_assignments


def process_bandwidth(a_course, a_assignment_group_id, a_level_serie_collection, a_file_name):
    assignment_group = a_course.get_assignment_group(a_assignment_group_id)
    if not assignment_group.bandwidth:
        print("BPB06 - No bandwidth defined in perspective", assignment_group.name)
    # print("BPB07 - Processing", a_assignment_group.name, "strategy", a_assignment_group.strategy)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(height=800, width=1200, showlegend=False)
    plot_bandbreedte_colored(0, 0, fig, a_course.days_in_semester, assignment_group.bandwidth, False,
                             assignment_group.total_points)
    fig.update_layout(title=f"{assignment_group.name}, strategy {assignment_group.strategy}", showlegend=False)
    fig.update_yaxes(title_text="Punten", range=[0, assignment_group.total_points])
    fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester])
    plot_assignments(0, 0, fig, a_course, True, assignment_group.assignment_sequences, a_level_serie_collection)
    fig.write_html(a_file_name, include_plotlyjs="cdn")


def process_bandwidth_overall(a_course, a_level_serie_collection, a_file_name):
    for perspective_id in a_course.perspectives:
        perspective = a_course.perspectives[perspective_id]
    if not perspective.bandwidth:
        print("BPB06 - No bandwidth defined in perspective", perspective.name)
    # print("BPB07 - Processing", a_assignment_group.name, "strategy", a_assignment_group.strategy)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(height=800, width=1200, showlegend=False)
    plot_bandbreedte_colored(0, 0, fig, a_course.days_in_semester, perspective.bandwidth, False,
                             perspective.total_points)
    fig.update_layout(title=f"{perspective.name}", showlegend=False)
    fig.update_yaxes(title_text="Punten", range=[0, perspective.total_points])
    fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester])
    # plot_assignments(0, 0, fig, a_course, True, assignment_group.assignment_sequences, a_level_serie_collection)
    fig.write_html(a_file_name, include_plotlyjs="cdn")

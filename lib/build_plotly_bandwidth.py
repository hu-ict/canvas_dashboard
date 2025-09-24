from plotly.subplots import make_subplots
from lib.build_plotly_generic import plot_bandbreedte_colored
from lib.build_plotly_perspective import plot_assignments


def process_bandwidth(a_course, a_pespective, a_labels_colors, a_file_name):
    if len(a_pespective.bandwidth.points) == 0:
        print("BPB06 - No bandwidth defined in perspective", a_pespective.name)
    # print("BPB07 - Processing", a_assignment_group.name, "strategy", a_assignment_group.strategy)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.update_layout(height=800, width=1200, showlegend=False)
    plot_bandbreedte_colored(0, 0, fig, a_course.days_in_semester, a_pespective.bandwidth, False,
                             a_pespective.total_points)
    fig.update_layout(title=f"{a_pespective.name}, strategy a_pespective.strategy", showlegend=False)
    fig.update_yaxes(title_text="Punten", range=[0, a_pespective.total_points])
    fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester])
    plot_assignments(0, 0, fig, a_course, True, a_pespective.assignment_sequences, a_labels_colors)
    fig.write_html(a_file_name, include_plotlyjs="cdn")

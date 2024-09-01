import sys

from plotly.subplots import make_subplots

from lib.build_plotly_perspective import plot_bandbreedte_colored, plot_assignments
from lib.file import read_start, read_course, read_course_instance, read_levels
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import get_actual_date, get_date_time_loc
from lib.translation_table import translation_table


def process_bandwidth(a_instances, a_start, a_course, a_assignment_group, a_labels_colors):
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
    if False:
        fig.update_yaxes(title_text="Voortgang", range=[0, 1], dtick=1)
    fig.update_yaxes(title_text="Punten", range=[0, a_assignment_group.total_points])
    fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester])

    plot_assignments(0, 0, fig, a_start, a_course, True, a_assignment_group.assignment_sequences, a_labels_colors)

    file_name = a_instances.get_html_path() + "bandwidth_"+str(a_assignment_group.id)
    asci_file_name = file_name.translate(translation_table)
    fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
    fig.write_image(asci_file_name + ".jpeg")


def main(instance_name):
    g_actual_date = get_actual_date()
    actual_date = get_date_time_loc(g_actual_date)
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("TB02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(start.course_file_name)
    labels_colors = read_levels("levels.json")
    for assignment_group in course.assignment_groups:
        print("TB11 -", assignment_group.name)
        if assignment_group.strategy == "NONE":
            assignment_group.bandwidth = None
        else:
            assignment_group.bandwidth = bandwidth_builder(assignment_group, course.days_in_semester)
            process_bandwidth(instances, start, course, assignment_group, labels_colors)
    if course.attendance is not None:
        process_bandwidth(instances, start, course, course.attendance, labels_colors)

    print("TB99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("TB01 - test_bandwidth.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

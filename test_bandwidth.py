import json
import sys

import plotly.graph_objs as go
from lib.build_plotly_perspective import plot_bandbreedte_colored, plot_open_assignments
from lib.file import read_start, read_course, read_course_instance, read_levels
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import get_actual_date, get_date_time_loc
from lib.translation_table import translation_table


def process_bandwidth(a_instances, a_start, a_course, a_perspective, a_labels_colors):
    for assignment_group_id in a_perspective.assignment_groups:
        assignment_group = a_course.find_assignment_group(assignment_group_id)
        if assignment_group is None:
            print("TB05 - ERROR assignment_group not found", assignment_group_id, "for perspective", a_perspective.name)
            return
        if assignment_group.strategy == "NONE":
            print("TB06 - No strategy defined for", assignment_group_id, "in perspective", a_perspective.name)
            continue
        print("TB07 - Processing", assignment_group_id, "in perspective", a_perspective.name, "strategy", assignment_group.strategy)

        fig = go.Figure()
        plot_bandbreedte_colored(0, 0, fig, a_course.days_in_semester, assignment_group, False)

        fig.update_layout(title=f"{assignment_group.name}, strategy {assignment_group.strategy}",
                          showlegend=False)
        if False:
            fig.update_yaxes(title_text="Voortgang", range=[0, 1], dtick=1)
        fig.update_yaxes(title_text="Punten", range=[0, assignment_group.total_points])
        fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, a_course.days_in_semester])

        plot_open_assignments(0, 0, fig, a_start, True, assignment_group.assignments, a_labels_colors)

        file_name = a_instances.get_test_path() + assignment_group.name.lower()
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
        if assignment_group.strategy == "NONE":
            assignment_group.bandwidth = None
        else:
            assignment_group.bandwidth = bandwidth_builder(assignment_group, course.days_in_semester)

    process_bandwidth(instances, start, course, course.attendance, labels_colors)
    for perspective in course.perspectives.values():
        process_bandwidth(instances, start, course, perspective, labels_colors)

    print("TB99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("TB01 - test_bandwidth.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

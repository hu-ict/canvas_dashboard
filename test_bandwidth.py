import json
import sys

import plotly.graph_objs as go
from lib.build_plotly_perspective import plot_bandbreedte_colored, plot_open_assignments
from lib.file import read_start, read_course, read_progress, read_results, read_course_instance, read_labels_colors
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import get_actual_date
from lib.translation_table import translation_table


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(start.course_file_name)
    labels_colors = read_labels_colors("labels_colors.json")
    for assignment_group in course.assignment_groups:
        assignment_group.assignments = sorted(assignment_group.assignments, key=lambda a: a.assignment_day)
        if assignment_group.strategy == "NONE":
            assignment_group.bandwidth = None
        else:
            assignment_group.bandwidth = bandwidth_builder(assignment_group, course.days_in_semester)
    for assignment_group in course.assignment_groups:
        if assignment_group.strategy == "NONE":
            continue
        fig = go.Figure()
        plot_bandbreedte_colored(0, 0, fig, course.days_in_semester, assignment_group, False)
        fig.update_layout(title = assignment_group.name+ ", strategy " + assignment_group.strategy)

        if False:
            fig.update_yaxes(title_text="Voortgang", range=[0, 1], dtick=1)
        # elif a_perspective.name == a_start.attendance_perspective:
        #     a_fig.update_yaxes(title_text="Percentage aanwezig", range=[0, l_assignment_group.total_points], row=a_row,
        #                        col=a_col)
        else:
            fig.update_yaxes(title_text="Punten", range=[0, assignment_group.total_points])
        fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, course.days_in_semester])

        plot_open_assignments(0, 0, fig, start, True, assignment_group.assignments, labels_colors)

        file_name = instances.get_test_path() + assignment_group.name.lower()
        asci_file_name = file_name.translate(translation_table)
        fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
        fig.write_image(asci_file_name + ".jpeg")

    with open(start.course_file_name, 'w') as f:
        dict_result = course.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)
    print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("test_bandwidth.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
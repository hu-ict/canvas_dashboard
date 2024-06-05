import json
import sys

import plotly.graph_objs as go
from lib.build_plotly_perspective import plot_bandbreedte_colored, plot_open_assignments
from lib.file import read_start, read_course, read_course_instance, read_levels
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import get_actual_date, get_date_time_loc
from lib.translation_table import translation_table


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(start.course_file_name)
    labels_colors = read_levels("levels.json")
    for assignment_group in course.assignment_groups:
        if assignment_group.strategy == "NONE":
            assignment_group.bandwidth = None
        else:
            assignment_group.bandwidth = bandwidth_builder(assignment_group, course.days_in_semester)
    for perspective in course.perspectives.values():
        for assignment_group_id in perspective.assignment_groups:
            assignment_group = course.find_assignment_group(assignment_group_id)
            if assignment_group.strategy == "NONE":
                continue
            fig = go.Figure()
            plot_bandbreedte_colored(0, 0, fig, course.days_in_semester, assignment_group, False)
            actual_date = get_date_time_loc(g_actual_date)
            fig.update_layout(title=f"{assignment_group.name}, strategy {assignment_group.strategy}, versie {actual_date}", showlegend=False)
            if False:
                fig.update_yaxes(title_text="Voortgang", range=[0, 1], dtick=1)
            fig.update_yaxes(title_text="Punten", range=[0, assignment_group.total_points])
            fig.update_xaxes(title_text="Dagen in onderwijsperiode", range=[0, course.days_in_semester])

            plot_open_assignments(0, 0, fig, start, True, assignment_group.assignments, labels_colors)

            file_name = instances.get_test_path() + assignment_group.name.lower()
            asci_file_name = file_name.translate(translation_table)
            fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
            fig.write_image(asci_file_name + ".jpeg")
    # genereer ook attendance

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

import sys

from plotly.subplots import make_subplots

from lib.build_plotly_bandwidth import process_bandwidth
from lib.build_plotly_perspective import plot_bandbreedte_colored, plot_assignments
from lib.file import read_start, read_course, read_course_instance, read_levels
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import get_actual_date, get_date_time_loc
from lib.translation_table import translation_table


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

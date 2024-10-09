import sys

from canvasapi import Canvas
from plotly.subplots import make_subplots

from lib.build_bootstrap_student import build_bootstrap_student_index
from lib.build_plotly_attendance import plot_attendance
from lib.build_plotly_perspective import plot_perspective, find_submissions, plot_overall_peilingen

from lib.lib_bootstrap import load_templates
from lib.lib_date import get_date_time_loc, get_actual_date, API_URL
from lib.file import read_start, read_course, read_results, read_course_instance, read_levels_from_canvas, read_levels


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GP02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    templates = load_templates(instances.get_template_path())
    level_series = read_levels("levels.json")

    for student in results.students:
        # print(l_peil_construction)
        print("GP10 -", student.name)

        build_bootstrap_student_index(instances, results.id, course, student, results.actual_date, templates, level_series)
    print("GP99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GP01 - generate_portfolio.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

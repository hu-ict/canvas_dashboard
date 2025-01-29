import sys
from canvasapi import Canvas

from generate_plotly import generate_plotly
from lib.build_bootstrap_student import build_bootstrap_student_index
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_actual_date, API_URL
from lib.file import read_course, read_results, read_course_instances, read_levels_from_canvas, read_start


def generate_portfolio(instance_name):
    print("GPF01 - generate_portfolio.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("GPF02 - Instance:", instance.name)
    course = read_course(instance.get_course_file_name())
    results = read_results(instance.get_result_file_name())
    templates = load_templates(instance.get_template_path())
    # level_serie_collection = read_levels("levels.json")
    start = read_start(instance.get_start_file_name())
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GRF03 - Username", user.name)
    canvas_course = canvas.get_course(course.canvas_id)
    level_serie_collection = read_levels_from_canvas(canvas_course)

    for student in results.students:
        # print(l_peil_construction)
        print("GPF10 -", student.name)

        build_bootstrap_student_index(instance, results.id, course, student, results.actual_date, results.actual_day, templates, level_serie_collection)
    print("GPF99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_plotly(sys.argv[1])
        generate_portfolio(sys.argv[1])
    else:
        generate_plotly("")
        generate_portfolio("")

import sys
from canvasapi import Canvas
from lib.build_bootstrap_student import build_bootstrap_student_index
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_actual_date, API_URL
from lib.file import read_course, read_results, read_course_instance, read_levels, read_levels_from_canvas, read_start


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GP02 - Instance:", instances.current_instance)
    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    templates = load_templates(instances.get_template_path())
    # level_serie_collection = read_levels("levels.json")
    start = read_start(instances.get_start_file_name())
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GR03 - Username", user.name)
    canvas_course = canvas.get_course(course.canvas_id)
    level_serie_collection = read_levels_from_canvas(canvas_course)

    for student in results.students:
        # print(l_peil_construction)
        print("GP10 -", student.name)

        build_bootstrap_student_index(instances, results.id, course, student, results.actual_date, results.actual_day, templates, level_serie_collection)
    print("GP99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GP01 - generate_portfolio.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

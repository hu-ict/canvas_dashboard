import json
import sys

from scripts.lib.build_bootstrap_student import build_bootstrap_student_index
from scripts.lib.lib_bootstrap import load_templates
from scripts.lib.lib_date import get_actual_date
from scripts.lib.file import read_course, read_results, read_environment, read_dashboard
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, DIR_DIV


def generate_portfolio(course_code, instance_name):
    print("GPL01 - generate_portfolio.py")
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    print("Instance:", course_instance.name)

    course = read_course(course_instance.get_course_file_name())
    results = read_results(course_instance.get_result_file_name())
    dashboard = read_dashboard(course_instance.get_dashboard_file_name())

    templates = load_templates("templates" + DIR_DIV)
    for student in results.students:
        # print(l_peil_construction)
        print("GPF11 -", student.name)
        build_bootstrap_student_index(course_instance, results.id, course, student, results.actual_date, results.actual_day, templates, dashboard)
    print("GPF99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # generate_plotly(sys.argv[1])
        generate_portfolio(sys.argv[1], sys.argv[2])
    else:
        # generate_plotly("")
        generate_portfolio("", "")

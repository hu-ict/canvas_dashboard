import json
import sys

from scripts.lib.build_bootstrap_student import build_bootstrap_student_index
from scripts.lib.lib_bootstrap import load_templates
from scripts.lib.lib_date import get_actual_date
from scripts.lib.file import read_course, read_results, read_environment, read_dashboard
from scripts.lib.file_const import DIR_DIV


def generate_portfolio(course_instance):
    print("GPL01 - generate_portfolio.py")
    g_actual_date = get_actual_date()
    course = read_course(course_instance.get_course_file_name())
    results = read_results(course_instance.get_result_file_name())
    dashboard = read_dashboard(course_instance.get_dashboard_file_name())

    templates = load_templates("scripts" + DIR_DIV + "templates" + DIR_DIV)
    for student in results.students:
        # print(l_peil_construction)
        print("GPF11 -", student.name)
        build_bootstrap_student_index(course_instance, results.id, course, student, results.actual_date, results.actual_day, templates, dashboard)
    print("GPF99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


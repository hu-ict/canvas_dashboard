import sys

from plotly.subplots import make_subplots

from lib.build_bootstrap import build_bootstrap_portfolio
from lib.build_plotly_attendance import plot_attendance
from lib.build_plotly_perspective import plot_perspective, find_submissions, plot_overall_peilingen
from lib.build_plotly_portfolio_items import build_portfolio_items
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_date_time_loc, get_actual_date
from lib.file import read_start, read_course, read_results, read_levels, read_course_instance
from lib.translation_table import translation_table
from model.Submission import Submission


def write_student_portfolio(a_instances, a_course, a_student, a_actual_date, a_templates, a_levels):
    build_bootstrap_portfolio(a_instances, a_course, a_student, a_actual_date, a_templates, a_levels)



def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GP02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(instances.get_course_file_name(instances.current_instance))
    if len(course.learning_outcomes) == 0:
        return
    results = read_results(instances.get_result_file_name(instances.current_instance))
    templates = load_templates(instances.get_template_path())
    levels = read_levels("levels.json")

    if results.actual_day > course.days_in_semester:
        course.days_in_semester = results.actual_day + 1

    count = 0
    for student in results.students:
        # print(l_peil_construction)
        print("GP10 -", student.name)
        write_student_portfolio(instances, course, student, results.actual_date, templates, levels)
        build_portfolio_items(instances, course, student, levels)

    print("GP99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GP01 - generate_portfolio.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

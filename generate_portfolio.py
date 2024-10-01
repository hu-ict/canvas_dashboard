import sys

from plotly.subplots import make_subplots

from lib.build_bootstrap import build_bootstrap_portfolio, build_bootstrap_student_index, \
    build_bootstrap_portfolio_empty
from lib.build_plotly_attendance import plot_attendance
from lib.build_plotly_perspective import plot_perspective, find_submissions, plot_overall_peilingen

from lib.lib_bootstrap import load_templates
from lib.lib_date import get_date_time_loc, get_actual_date
from lib.file import read_start, read_course, read_results, read_levels, read_course_instance
from lib.translation_table import translation_table
from model.Submission import Submission

def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GP02 - Instance:", instances.current_instance)
    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    templates = load_templates(instances.get_template_path())
    levels = read_levels("levels.json")

    for student in results.students:
        # print(l_peil_construction)
        print("GP10 -", student.name)
        if len(course.learning_outcomes) > 0:
            build_bootstrap_portfolio(instances, course, student, results.actual_date, templates, levels)
        else:
            build_bootstrap_portfolio_empty(instances, course, student, results.actual_date, templates, levels)
        build_bootstrap_student_index(instances, course, student, results.actual_date, templates, levels)


    print("GP99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GP01 - generate_portfolio.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

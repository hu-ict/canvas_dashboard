import json
import os
import sys


from lib.build_bootstrap_werkvoorraad import build_bootstrap_canvas_workload_general
from lib.build_late import build_bootstrap_teacher_index
from lib.build_total_progress import create_total_progress, process_total_progress
from lib.build_total_workload import get_teachers, create_workload, get_workload
from lib.build_bootstrap import build_bootstrap_general
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_actual_date, API_URL
from lib.plot_totals import plot_werkvoorraad, plot_voortgang, plot_overall_opbouw
from lib.file import read_course, read_results, read_workload, read_dashboard_from_canvas, read_progress_history, \
    read_environment, read_secret_api_key, read_dashboard
from model.environment.Environment import ENVIRONMENT_FILE_NAME
from model.environment.SecretApiKey import SECRET_API_KEY_FILE_NAME
from model.workload.WorkloadDay import WorkloadDay


def generate_dashboard(course_code, instance_name):
    print("GCF01 - generate_dashboard.py")
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    # secret_api_key = read_secret_api_key(SECRET_API_KEY_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    print("Instance:", course_instance.name)

    #conversie: temp directory is nodig in nieuwe versie, maakt aan als deze nog niet bestaat
    os.makedirs(os.path.dirname(course_instance.get_temp_path()), exist_ok=True)

    print("GD02 - Instance:", course_instance.name)
    course = read_course(course_instance.get_course_file_name())
    results = read_results(course_instance.get_result_file_name())
    templates = load_templates("templates//")
    dashboard = read_dashboard(course_instance.get_dashboard_file_name())
    print("GD02 - create_total_progress(instance, course)")
    total_progress = create_total_progress(course)
    print("GD03 - create_total_workload(instance, course, team_coaches)")
    process_total_progress(course_instance, course, results, total_progress)
    teachers = get_teachers(course)

    print("GD04 - create_total_workload(instance, course, team_coaches)")
    workload = create_workload(teachers)
    print("GD05 - process_total_workload(instance, course, results, total_workload)")
    workload = get_workload(course, results, workload)

    workload_history = read_workload(course_instance.get_workload_file_name())
    workload_day = WorkloadDay(results.actual_day)
    workload_day.from_actual_workload(workload)
    workload_history.append_day(workload_day)
    with open(course_instance.get_workload_file_name(), 'w') as f:
        dict_result = workload_history.to_json()
        json.dump(dict_result, f, indent=2)
    print("GD09 - Plot werkvoorraad")
    plot_werkvoorraad(course_instance, course, workload, workload_history)
    plot_overall_opbouw(course_instance, course, dashboard.level_serie_collection)
    print("GD08 - build_late_email(instance, templates, course, results, student_totals)")

    # recipients_cc = "karin.elich@hu.nl"
    # recipients = ""
    # workload_email(recipients, recipients_cc, build_problems(course, templates, total_workload))

    build_bootstrap_canvas_workload_general(course_instance, course, workload, results.actual_date, templates)
    print("GD06 - build_bootstrap_general(start, course, results, team_coaches, labels_colors)")
    build_bootstrap_general(course_instance, course, results, templates, teachers, dashboard.level_serie_collection, workload)
    print("GD07 - build_bootstrap_teacher_index(instances, templates, course, results, workload)")
    build_bootstrap_teacher_index(course_instance, templates, course, results, workload)

    with open("total_progress.json", 'w') as f:
        dict_result = total_progress
        json.dump(dict_result, f, indent=2)
    print("GD10 - Generate voortgang")
    plot_voortgang(course_instance, course, total_progress, read_progress_history(course_instance.get_progress_file_name()),
                   dashboard.level_serie_collection.level_series['progress'], dashboard.level_serie_collection.level_series['grade'])

    print("GD99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_dashboard(sys.argv[1], sys.argv[2])
    else:
        generate_dashboard("", "")

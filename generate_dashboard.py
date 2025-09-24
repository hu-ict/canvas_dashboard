import json
import os
import sys

from canvasapi import Canvas

from lib.build_bootstrap_werkvoorraad import build_bootstrap_canvas_werkvoorraad_index
from lib.build_late import build_bootstrap_late_submission_list
from lib.build_total_progress import create_total_progress, process_total_progress
from lib.build_total_workload import get_teachers, create_workload, get_workload
from lib.build_bootstrap import build_bootstrap_general
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_actual_date, API_URL
from lib.plot_totals import plot_werkvoorraad, plot_voortgang
from lib.file import read_course, read_results, read_progress, read_course_instances, read_workload, read_start, read_dashboard_from_canvas
from model.workload.WorkloadDay import WorkloadDay


def generate_dashboard(instance_name):
    print("GD01 - generate_dashboard.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    #conversie: temp directory is nodig in nieuwe versie, maakt aan als nog niet bestaand
    os.makedirs(os.path.dirname(instance.get_temp_path()), exist_ok=True)

    print("GD02 - Instance:", instance.name)
    course = read_course(instance.get_course_file_name())
    results = read_results(instance.get_result_file_name())
    templates = load_templates(instance.get_template_path())
    # level_serie_collection = read_levels("levels.json")
    start = read_start(instance.get_start_file_name())
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GR01 - Username", user.name)
    canvas_course = canvas.get_course(course.canvas_id)
    dashboard = read_dashboard_from_canvas(canvas_course)
    print("GD02 - create_total_progress(instance, course)")
    total_progress = create_total_progress(instance, course)
    print("GD03 - create_total_workload(instance, course, team_coaches)")
    process_total_progress(instance, course, results, total_progress)
    teachers = get_teachers(course)

    print("GD04 - create_total_workload(instance, course, team_coaches)")
    workload = create_workload(teachers)
    print("GD05 - process_total_workload(instance, course, results, total_workload)")
    workload = get_workload(course, results, workload)

    workload_history = read_workload(instance.get_workload_file_name())
    workload_day = WorkloadDay(results.actual_day)
    workload_day.from_actual_workload(workload)
    workload_history.append_day(workload_day)
    with open(instance.get_workload_file_name(), 'w') as f:
        dict_result = workload_history.to_json()
        json.dump(dict_result, f, indent=2)
    print("GD09 - Plot werkvoorraad")
    plot_werkvoorraad(instance, course, workload, workload_history)
    print("GD08 - build_late_email(instance, templates, course, results, student_totals)")

    # recipients_cc = "karin.elich@hu.nl"
    # recipients = ""
    # workload_email(recipients, recipients_cc, build_problems(course, templates, total_workload))

    build_bootstrap_canvas_werkvoorraad_index(instance, course, workload, results.actual_date, templates)
    print("GD06 - build_bootstrap_general(start, course, results, team_coaches, labels_colors)")
    build_bootstrap_general(instance, course, results, templates, teachers, dashboard.level_serie_collection, workload)
    print("GD07 - build_late(instances, templates, results, student_totals)")
    build_bootstrap_late_submission_list(instance, templates, course, results, workload)

    with open("total_progress.json", 'w') as f:
        dict_result = total_progress
        json.dump(dict_result, f, indent=2)
    print("GD10 - Generate voortgang")
    plot_voortgang(instance, course, total_progress, read_progress(instance.get_progress_file_name()),
                   dashboard.level_serie_collection.level_series['progress'], dashboard.level_serie_collection.level_series['grade'])
    print("GD99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_dashboard(sys.argv[1])
    else:
        generate_dashboard("")

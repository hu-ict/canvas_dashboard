import json
import os
import sys

from canvasapi import Canvas

from lib.build_bootstrap_werkvoorraad import build_bootstrap_canvas_werkvoorraad_index
from lib.build_late import build_bootstrap_late_list
from lib.build_total_progress import create_total_progress, process_total_progress
from lib.build_total_workload import init_teachers_dict, create_total_workload, process_total_workload, build_late_email
from lib.build_bootstrap import build_bootstrap_general
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_actual_date, API_URL
from lib.plot_totals import plot_werkvoorraad, plot_voortgang
from lib.file import read_course, read_results, read_progress, read_course_instances, read_workload, read_levels_from_canvas, read_start
from model.WorkloadDay import WorkloadDay


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
    level_serie_collection = read_levels_from_canvas(canvas_course)
    print("GD02 - create_total_progress(instance, course)")
    total_progress = create_total_progress(instance, course)
    print("GD03 - create_total_workload(instance, course, team_coaches)")
    process_total_progress(instance, course, results, total_progress)
    project_teachers = init_teachers_dict(course, course.project_groups)
    guild_teachers = init_teachers_dict(course, course.guild_groups)
    print("GD04 - create_total_workload(instance, course, team_coaches)")
    total_workload = create_total_workload(instance, course, project_teachers, guild_teachers)
    print("GD05 - process_total_workload(instance, course, results, total_workload)")
    process_total_workload(instance, course, results, total_workload)
    with open("total_workload.json", 'w') as f:
        dict_result = total_workload
        json.dump(dict_result, f, indent=2)
    workload_history = read_workload(instance.get_workload_file_name())
    workload_day = WorkloadDay(results.actual_day)
    workload_day.from_actual_workload(total_workload)
    workload_history.append_day(workload_day)
    with open(instance.get_workload_file_name(), 'w') as f:
        dict_result = workload_history.to_json()
        json.dump(dict_result, f, indent=2)
    print("GD09 - Plot werkvoorraad")
    plot_werkvoorraad(instance, course, total_workload, workload_history)
    print("GD08 - build_late_email(instance, templates, course, results, student_totals)")
    build_late_email(course, total_workload)
    build_bootstrap_canvas_werkvoorraad_index(instance, course, results.actual_date, templates, total_workload)
    print("GD06 - build_bootstrap_general(start, course, results, team_coaches, labels_colors)")
    build_bootstrap_general(instance, course, results, templates, project_teachers, level_serie_collection, total_workload)
    print("GD07 - build_late(instances, templates, results, student_totals)")
    build_bootstrap_late_list(instance, templates, course, results, total_workload)

    with open("total_progress.json", 'w') as f:
        dict_result = total_progress
        json.dump(dict_result, f, indent=2)


    print("GD10 - Generate voortgang")
    plot_voortgang(instance, course, total_progress, read_progress(instance.get_progress_file_name()),
                   level_serie_collection.level_series['progress'], level_serie_collection.level_series['grade'])
    print("GD99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_dashboard(sys.argv[1])
    else:
        generate_dashboard("")

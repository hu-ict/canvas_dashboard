import json
import os
import sys

from canvasapi import Canvas

from lib.build_totals import build_totals, create_student_totals, init_coaches_dict
from lib.build_bootstrap import build_bootstrap_general
from lib.build_late import build_late_list
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_actual_date, API_URL
from lib.plot_totals import plot_werkvoorraad, plot_voortgang
from lib.file import read_course, read_results, read_progress, read_course_instances, read_workload, \
    read_levels_from_canvas, read_start
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
    # for teacher in course.teachers:
    #     print(teacher)
    results = read_results(instance.get_result_file_name())
    templates = load_templates(instance.get_template_path())
    # level_serie_collection = read_levels("levels.json")
    start = read_start(instance.get_start_file_name())
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GR03 - Username", user.name)
    canvas_course = canvas.get_course(course.canvas_id)
    level_serie_collection = read_levels_from_canvas(canvas_course)

    team_coaches = init_coaches_dict(course)
    # for team_coach in team_coaches.values():
    #     print(team_coach['teacher'])

    student_totals = create_student_totals(instance, course, team_coaches)
    with open("student_totals.json", 'w') as f:
        dict_result = student_totals
        json.dump(dict_result, f, indent=2)


    # with open("dump.json", 'w') as f:
    #     dict_result = json.dumps(student_totals, indent = 4)
    #     json.dump(student_totals, f, indent=2)

    # print("GD04", student_totals)
    print("GD05 - build_totals(start, course, results, student_totals, gilde, team_coaches)")
    build_totals(instance, course, results, student_totals)
    print("GD06 - build_bootstrap_general(start, course, results, team_coaches, labels_colors)")
    build_bootstrap_general(instance, course, results, templates, team_coaches, level_serie_collection, student_totals)
    print("GD07 - build_late(instances, templates, results, student_totals)")
    build_late_list(instance, templates, results, student_totals)
    with open("student_totals.json", 'w') as f:
        dict_result = student_totals
        json.dump(dict_result, f, indent=2)

    workload_history = read_workload(instance.get_workload_file_name())
    workload_day = WorkloadDay(results.actual_day)
    workload_day.from_late_list(student_totals["late"]["count"])
    workload_history.append_day(workload_day)

    with open(instance.get_workload_file_name(), 'w') as f:
        dict_result = workload_history.to_json()
        json.dump(dict_result, f, indent=2)

    plot_werkvoorraad(instance, course, student_totals, workload_history)
    plot_voortgang(instance, course, student_totals, read_progress(instance.get_progress_file_name()),
                   level_serie_collection.level_series['progress'])
    print("GD99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_dashboard(sys.argv[1])
    else:
        generate_dashboard("")

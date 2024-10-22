import json
import sys

from canvasapi import Canvas

from lib.build_totals import build_totals, create_student_totals, init_coaches_dict
from lib.build_bootstrap import build_bootstrap_general
from lib.build_late import build_late_list
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_actual_date, API_URL
from lib.plot_totals import plot_werkvoorraad, plot_voortgang
from lib.file import read_course, read_results, read_progress, read_course_instance, read_workload, \
    read_levels_from_canvas, read_levels, read_start
from model.WorkloadDay import WorkloadDay





def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GD02 - Instance:", instances.current_instance, instances.get_category(instances.current_instance))
    course = read_course(instances.get_course_file_name(instances.current_instance))
    for teacher in course.teachers:
        print(teacher)
    results = read_results(instances.get_result_file_name(instances.current_instance))
    templates = load_templates(instances.get_template_path())
    # level_serie_collection = read_levels("levels.json")
    start = read_start(instances.get_start_file_name())
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GR03 - Username", user.name)
    canvas_course = canvas.get_course(course.canvas_id)
    level_serie_collection = read_levels_from_canvas(canvas_course)

    team_coaches = init_coaches_dict(course)
    for team_coach in team_coaches.values():
        print(team_coach['teacher'])

    student_totals = create_student_totals(instances, course, team_coaches)
    with open("student_totals.json", 'w') as f:
        dict_result = student_totals
        json.dump(dict_result, f, indent=2)


    # with open("dump.json", 'w') as f:
    #     dict_result = json.dumps(student_totals, indent = 4)
    #     json.dump(student_totals, f, indent=2)

    # print("GD04", student_totals)
    print("GD05 - build_totals(start, course, results, student_totals, gilde, team_coaches)")
    build_totals(instances, course, results, student_totals)
    print("GD06 - build_bootstrap_general(start, course, results, team_coaches, labels_colors)")
    build_bootstrap_general(instances, course, results, templates, team_coaches, level_serie_collection, student_totals)
    print("GD07 - build_late(instances, templates, results, student_totals)")
    build_late_list(instances, templates, results, student_totals)
    with open("student_totals.json", 'w') as f:
        dict_result = student_totals
        json.dump(dict_result, f, indent=2)

    workload_history = read_workload(instances.get_workload_file_name(instances.current_instance))
    workload_day = WorkloadDay(results.actual_day)
    workload_day.from_late_list(student_totals["late"]["count"])
    workload_history.append_day(workload_day)

    with open(instances.get_workload_file_name(instances.current_instance), 'w') as f:
        dict_result = workload_history.to_json()
        json.dump(dict_result, f, indent=2)

    plot_werkvoorraad(instances, course, student_totals, workload_history)
    plot_voortgang(instances, course, student_totals, read_progress(instances.get_progress_file_name(instances.current_instance)), level_serie_collection.level_series['progress'])
    print("GD99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GD01 - generate_dashboard.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

import json
import os
import sys

from scripts.lib.build_bootstrap import build_bootstrap_dashboard_index
from scripts.lib.build_bootstrap_release_planning import build_release_planning_index_html
from scripts.lib.build_bootstrap_werkvoorraad import build_workload_index_html
from scripts.lib.build_late import build_teacher_index_html
from scripts.lib.build_plotly_bandwidth import build_plotly_bandwidth
from scripts.lib.build_total_progress import create_total_progress, process_total_progress
from scripts.lib.build_total_workload import get_teachers, create_workload, get_workload
from scripts.lib.lib_bootstrap import load_templates
from scripts.lib.lib_date import get_actual_date
from scripts.lib.plot_totals import build_plotly_workload, build_plotly_progress
from scripts.lib.file import read_course, read_results, read_workload, read_progress_history, read_dashboard
from scripts.model.workload.WorkloadDay import WorkloadDay


def generate_dashboard(course_instance):
    print("GPL01 - generate_dashboard.py")
    g_actual_date = get_actual_date()

    #conversie: temp directory is nodig in nieuwe versie, maakt aan als deze nog niet bestaat
    os.makedirs(os.path.dirname(course_instance.get_temp_path()), exist_ok=True)

    print("GD02 - Instance:", course_instance.name)
    course = read_course(course_instance.get_course_file_name())
    results = read_results(course_instance.get_result_file_name())
    templates = load_templates("scripts//templates//")
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
    print("GD08 - build_plotly_workload")
    build_plotly_workload(course_instance, course, workload)
    print("GD09 - build_plotly_bandwidth")
    build_plotly_bandwidth(course_instance, course, dashboard.level_serie_collection)

    print("GD10 - plot_voortgang")
    build_plotly_progress(course_instance, course, total_progress, read_progress_history(course_instance.get_progress_file_name()),
                   dashboard.level_serie_collection.level_series['progress'], dashboard.level_serie_collection.level_series['grade'])
    print("GD08 - build_late_email(instance, templates, course, results, student_totals)")

    with open("total_progress.json", 'w') as f:
        dict_result = total_progress
        json.dump(dict_result, f, indent=2)

    # recipients_cc = "karin.elich@hu.nl"
    # recipients = ""
    # workload_email(recipients, recipients_cc, build_problems(course, templates, total_workload))

    build_workload_index_html(course_instance, course, workload, results.actual_date, templates)
    print("GD07 - build_teacher_index_html(instances, templates, course, results, workload)")
    build_teacher_index_html(course_instance, templates, dashboard, course, results, workload)
    print("GD08 - build_release_planning_index_html(course_instance, course, templates)")
    build_release_planning_index_html(course_instance, course, templates)
    print("GD19 - build_bootstrap_dashboard_indexcourse_instance, course, results, templates, teachers, dashboard, workload)")
    build_bootstrap_dashboard_index(course_instance, course, results, templates, teachers, dashboard, workload)

    print("GPL99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

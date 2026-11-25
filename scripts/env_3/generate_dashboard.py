import json
import os

from scripts.lib.lib_saturation import get_bof_saturation, get_y_max, get_student_saturations, get_portfolio_saturation, \
    get_teacher_portfolio_saturations
from scripts.lib.build_bootstrap import build_bootstrap_dashboard_index
from scripts.lib.build_bootstrap_release_planning import build_release_planning_index_html
from scripts.lib.build_bootstrap_werkvoorraad import build_workload_index_html
from scripts.lib.build_late import build_workload_item_index_html
from scripts.lib.build_plotly_bandwidth import build_plotly_bandwidth
from scripts.lib.build_plotly_saturation import process_plotly_single_saturation, process_plotly_single_distribution, \
    proces_student_saturations, proces_portfolio_saturation, proces_portfolio_teacher_saturation
from scripts.lib.build_total_progress import create_total_progress, process_total_progress
from scripts.lib.build_total_workload import get_teachers, create_workload, get_workload
from scripts.lib.lib_bootstrap import load_templates
from scripts.lib.lib_date import get_actual_date
from scripts.lib.plot_totals import build_plotly_workload, build_plotly_progress
from scripts.lib.file import read_course, read_results, read_workload, read_progress_history, read_dashboard, \
    write_results
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

    #******************************************
    # Learning_outcome saturation
    #******************************************
    get_bof_saturation(course, results)
    y_max = get_y_max(results)
    print("GDB02 - BOF_saturation:", results.get_learning_outcome("LU1").get_day(results.actual_day), len(results.get_learning_outcome("LU1").last_day_collection))
    process_plotly_single_saturation(course_instance, results.saturation_learning_outcomes, y_max +1)
    process_plotly_single_distribution(course_instance, results.saturation_learning_outcomes, y_max + 1, results.actual_day)
    for student in results.students:
        for learning_outcome in student.learning_outcomes.values():
            if len(learning_outcome.feedback_list) > results.get_learning_outcome(learning_outcome.id).get_day(results.actual_day).average:
                learning_outcome.saturation = 3
            elif len(learning_outcome.feedback_list) > results.get_learning_outcome(learning_outcome.id).get_day(results.actual_day).min_stdv:
                learning_outcome.saturation = 2
            else:
                learning_outcome.saturation = 1
    student_saturations = get_student_saturations(results)
    proces_student_saturations(course_instance, student_saturations, dashboard.level_serie_collection.level_series['progress'])
    portfolio_saturations = get_portfolio_saturation(course, results)
    for portfolio_saturation in portfolio_saturations.values():
        print("GDB31 - Saturations", portfolio_saturation)



    proces_portfolio_saturation(course_instance, portfolio_saturations)

    for teacher in course.teachers:
        teacher_portfolio_saturations = get_teacher_portfolio_saturations(teacher.id, course, results, portfolio_saturations)
        y_counts = []
        x_labels = []
        y_hover = []
        for teacher_portfolio_saturation in teacher_portfolio_saturations.values():
            portfolio_saturation = portfolio_saturations[teacher_portfolio_saturation.id]
            x_labels.append(teacher_portfolio_saturation.name)
            y_counts.append(teacher_portfolio_saturation.get_diff(portfolio_saturation.get_average_lu()))
            y_hover.append(str(teacher_portfolio_saturation.get_average_lu()))
        proces_portfolio_teacher_saturation(course_instance, teacher, x_labels, y_counts, y_hover)
    # ********************************************
    # Schrijf de resultaat.json voor elke student
    # ********************************************
    for student in results.students:
        # print(l_peil_construction)
        # print("GR41 -", student.name)
        student_name = student.email.split("@")[0].lower()
        file_name_json = course_instance.get_html_student_path() + student_name + ".json"
        with open(file_name_json, 'w', encoding='utf-8') as f:
            dict_result = student.to_json()
            json.dump(dict_result, f, indent=2)

    write_results(course_instance.get_result_file_name(), results)

    print("GD02 - create_total_progress(instance, course)")
    total_progress = create_total_progress(course)
    print("GD03 - create_total_workload(instance, course, team_coaches)")
    process_total_progress(course_instance, course, results, total_progress)

    teachers = get_teachers(course)
    print("GD04 - create_total_workload(instance, course, team_coaches)")
    workload = create_workload(dashboard, teachers, course.groups_1, course.groups_2)
    print("GD05 - process_total_workload(instance, course, results, total_workload)")
    workload = get_workload(course, results, workload)
    # workload = get_bof_value(course, results, workload)

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

    print("GDB09 - build_workload_index_html")
    build_workload_index_html(course_instance, course, workload, results.actual_date, templates)
    print("GDB10 - build_workload_item_index_html")
    build_workload_item_index_html(course_instance, templates, dashboard, course, results, workload)
    print("GDB11 - build_release_planning_index_html")
    build_release_planning_index_html(course_instance, course, templates)
    # print("GDB12 - build_analytics_index_html")
    # build_bootstrap_learning_analytics_index_html(course_instance, course, results, templates)
    print("GDB13 - build_bootstrap_dashboard_index")
    build_bootstrap_dashboard_index(course_instance, course, results, templates, teachers, dashboard, workload)
    # for teacher in workload.get_dimension("teachers").items:
    #     if teacher.total_value == 0:
    #         print("GDB20 - Teacher:", teacher.total_value)
    #     else:
    #         print(f"GDB22 - {teacher.name:30} {teacher.bof_count:4} {teacher.total_value:5} {int(teacher.bof_count*100/teacher.total_value):4}")

    print("GDB99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

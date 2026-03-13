import json
import sys

from plotly.subplots import make_subplots
from scripts.lib.build_plotly_attendance import plot_attendance_perspective
from scripts.lib.build_plotly_perspective import plot_perspective, plot_timeline
from scripts.lib.lib_date import get_date_time_loc, get_actual_date, get_time_div
from scripts.lib.file import read_course, read_results, read_dashboard


def plot_student(course_instance, course, student, actual_date, actual_day,
                 subplots,
                 level_serie_collection, feedback_colors, last_date):
    # last_date = get_time_div("11", last_date)
    fig = make_subplots(rows=subplots.rows, cols=subplots.cols, subplot_titles=subplots.titles, specs=subplots.specs,
                        vertical_spacing=0.10,
                        horizontal_spacing=0.08)
    fig.update_layout(height=900, width=1200, showlegend=False)

    for perspective in student.perspectives.values():
        if perspective.name in subplots.positions:
            row = subplots.positions[perspective.name]['row']
            col = subplots.positions[perspective.name]['col']
            # print("GP19 -", perspective, a_level_construction, a_grade_construction)
            plot_perspective(row, col, fig, course, perspective,
                             actual_day, get_date_time_loc(actual_date),
                             level_serie_collection)

    if "attendance" in subplots.positions:
        if course.attendance is not None:
            row = subplots.positions["attendance"]['row']
            col = subplots.positions["attendance"]['col']
            plot_attendance_perspective(row, col, fig, course, student.student_attendance, actual_day,
                                        get_date_time_loc(actual_date), level_serie_collection)
    # last_date = get_time_div("13", last_date)
    if "timeline" in subplots.positions:
        row = subplots.positions["timeline"]['row']
        col = subplots.positions["timeline"]['col']
        plot_timeline(row, col, fig, course, student, actual_day, get_date_time_loc(actual_date),
                      level_serie_collection, feedback_colors)
    # last_date = get_time_div("14", last_date)
    student_name = student.email.split("@")[0].lower()
    file_name_html = course_instance.get_temp_path() + student_name + "_progress.html"
    # last_date = get_time_div("17", last_date)
    fig.write_html(file_name_html, include_plotlyjs="cdn")
    # last_date = get_time_div("18", last_date)
    # if course_instance.course_code not in ["TICT-V1SE1-24"]:
    #     file_name_jpg = course_instance.get_html_student_path() + student_name + "_progress.jpg"
    #     fig.write_image(file_name_jpg)
    # # last_date = get_time_div("19", last_date)

def generate_plotly(course_instance):
    print("GPL01 - generate_plotly.py")
    g_actual_date = get_actual_date()
    course = read_course(course_instance.get_course_file_name())
    results = read_results(course_instance.get_result_file_name())
    dashboard = read_dashboard(course_instance.get_dashboard_file_name())
    if results.actual_day > course.days_in_semester:
        results.actual_day = course.days_in_semester

    last_date = g_actual_date
    for student in results.students:
        print("GPL90 -", student.name)
        plot_student(course_instance, course, student, results.actual_date, results.actual_day,
                     dashboard.subplot,
                     dashboard.level_serie_collection, dashboard.feedback_colors, last_date)
        # last_date = get_time_div("20", last_date)

    print("GPL99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


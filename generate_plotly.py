import sys
from canvasapi import Canvas
from plotly.subplots import make_subplots
from lib.build_plotly_attendance import plot_attendance_perspective
from lib.build_plotly_perspective import plot_perspective, plot_timeline
from lib.lib_date import get_date_time_loc, get_actual_date, API_URL
from lib.file import read_course, read_results, read_course_instances, read_start, read_dashboard_from_canvas


def plot_student(instances, course, student, actual_date, actual_day,
                 subplots,
                 level_serie_collection, feedback_colors):
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

    if "timeline" in subplots.positions:
        row = subplots.positions["timeline"]['row']
        col = subplots.positions["timeline"]['col']
        plot_timeline(row, col, fig, course, student, actual_day, get_date_time_loc(actual_date),
                      level_serie_collection, feedback_colors)

    student_name = student.email.split("@")[0].lower()
    file_name_html = instances.get_temp_path() + student_name + "_progress.html"
    fig.write_html(file_name_html, include_plotlyjs="cdn")
    if not instances.is_instance_of('prop_courses'):
        file_name_jpg = instances.get_student_path() + student_name + "_progress.jpg"
        fig.write_image(file_name_jpg)


def generate_plotly(instance_name):
    print("GPL01 - generate_plotly.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("GPL02 - Instance:", instance.name)
    course = read_course(instance.get_course_file_name())
    results = read_results(instance.get_result_file_name())
    # level_serie_collection = read_levels("levels.json")
    start = read_start(instance.get_start_file_name())
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GRL03 - Username", user.name)
    canvas_course = canvas.get_course(course.canvas_id)
    # level_serie_collection = read_levels_from_canvas(canvas_course)
    dashboard = read_dashboard_from_canvas(canvas_course)
    if results.actual_day > course.days_in_semester:
        results.actual_day = course.days_in_semester

    # Define bar properties

    # l_level_construction = level_construct(course)
    # l_grade_construction = grade_construct(course)
    count = 0
    for student in results.students:
        # l_level_construction = find_submissions(student, l_level_construction)
        # l_grade_construction = find_submissions(student, l_grade_construction)
        # print(l_peil_construction)
        print("GPL90 -", student.name)

        plot_student(instance, course, student, results.actual_date, results.actual_day,
                     dashboard.subplot,
                     dashboard.level_serie_collection, dashboard.feedback_colors)

    print("GPL99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_plotly(sys.argv[1])
    else:
        generate_plotly("")

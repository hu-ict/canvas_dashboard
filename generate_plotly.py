import sys

from canvasapi import Canvas
from plotly.subplots import make_subplots

from lib.build_plotly_attendance import plot_attendance_perspective
from lib.build_plotly_perspective import plot_perspective, find_submissions, plot_overall_level_moment, \
    plot_overall_grade_moment, plot_timeline
from lib.lib_date import get_date_time_loc, get_actual_date, API_URL
from lib.file import read_course, read_results, read_course_instances, read_start, read_dashboard_from_canvas
from model.Submission import Submission


def level_construct(a_course):
    l_peilingen = {}
    if a_course.level_moments is None or len(a_course.level_moments.assignment_groups) == 0:
        return l_peilingen
    for perspective in a_course.perspectives.values():
        l_peilingen[perspective.name] = []
    assignment_group = a_course.find_assignment_group(a_course.level_moments.assignment_groups[0])
    for assignment_sequence in assignment_group.assignment_sequences:
        for assignment in assignment_sequence.assignments:
            # zoek de juiste Assignment
            for peil_label in a_course.level_moments.moments:
                if peil_label.lower() in assignment.name.lower():
                    # zoek het juiste Perspective
                    for perspective_name in l_peilingen:
                        if perspective_name.lower() in assignment.name.lower():
                            l_peilingen[perspective_name].append({'assignment': assignment, 'submission': None})
    return l_peilingen


def grade_construct(a_course):
    l_grades = {}
    if a_course.level_moments is None or len(a_course.grade_moments.assignment_groups) == 0:
        return l_grades
    for perspective in a_course.perspectives.values():
        l_grades[perspective.name] = []
    assignment_group = a_course.find_assignment_group(a_course.grade_moments.assignment_groups[0])
    for assignment_sequence in assignment_group.assignment_sequences:
        for assignment in assignment_sequence.assignments:
            # zoek de juiste Assignment
            for peil_label in a_course.grade_moments.moments:
                if peil_label.lower() in assignment.name.lower():
                    # zoek het juiste Perspective
                    for perspective_name in l_grades:
                        if perspective_name.lower() in assignment.name.lower():
                            l_grades[perspective_name].append({'assignment': assignment, 'submission': None})
    return l_grades


def plot_student(instances, course, student, actual_date, actual_day,
                 a_level_construction, a_grade_construction,
                 subplots,
                 level_serie_collection):
    fig = make_subplots(rows=subplots.rows, cols=subplots.cols, subplot_titles=subplots.titles, specs=subplots.specs, vertical_spacing=0.10,
                        horizontal_spacing=0.08)


    fig.update_layout(height=900, width=1200, showlegend=False)
    for perspective in student.perspectives.values():
        row = subplots.positions[perspective.name]['row']
        col = subplots.positions[perspective.name]['col']
        # print("GP19 -", perspective, a_level_construction, a_grade_construction)
        plot_perspective(row, col, fig, course, perspective,
                         a_level_construction, a_grade_construction,
                         actual_day, get_date_time_loc(actual_date),
                         level_serie_collection)

    if course.attendance is not None:
        row = subplots.positions["attendance"]['row']
        col = subplots.positions["attendance"]['col']
        plot_attendance_perspective(row, col, fig, course, student.student_attendance, actual_day,
                                    get_date_time_loc(actual_date), level_serie_collection)

    if instances.is_instance_of('courses_2026'):
        row = subplots.positions["timeline"]['row']
        col = subplots.positions["timeline"]['col']
        plot_timeline(row, col, fig, course, student, level_serie_collection)

    if instances.is_instance_of('courses_2026'):
        for peil in course.level_moments.moments:
            print("GP21 - Peilmoment", peil, "overall", subplots.positions[peil]['row'], subplots.positions[peil]['col'])
            # overall peilmoment
            l_level_moment = student.get_level_moment_submission_by_query([peil])
            row = subplots.positions[peil]['row']
            col = subplots.positions[peil]['col']
            if l_level_moment is None:
                # nog niet ingevuld
                l_assignment = course.get_first_level_moment_by_query([peil])

                l_level_moment = Submission(0, 0, 0, 0,
                                            l_assignment.name, l_assignment.get_date(), l_assignment.get_day(),
                                            None, None,
                                            "1", False,
                                            None, None, None,
                                            -1, None, 3, 0)
            plot_overall_level_moment(row, col, fig, course, l_level_moment, level_serie_collection)

        for grade_moment in course.grade_moments.moments:
            # print("GP21 - Beordelingsmoment", grade_moment, "overall")
            l_grade_moment = student.get_grade_moment_submission_by_query([grade_moment])
            row = subplots.positions[grade_moment]['row']
            col = subplots.positions[grade_moment]['col']
            if l_grade_moment is None:
                # nog niet ingevuld
                l_assignment = course.get_first_grade_moment_by_query([grade_moment])
                l_grade_moment = Submission(0, 0, 0, 0,
                                            l_assignment.name, l_assignment.get_date(), l_assignment.get_day(),
                                            None, None,
                                            "1", False, None, None, None,
                                            -1, None, 3, 0)

            plot_overall_grade_moment(row, col, fig, course, l_grade_moment, level_serie_collection)
    if instances.is_instance_of('inno_courses'):
        # Peil overall drie peilmomenten
        for peil in course.level_moments.moments:
            print("GP21 - Peilmoment", peil, "overall", subplots.positions[peil]['row'], subplots.positions[peil]['col'])
            # overall peilmoment
            l_level_moment = student.get_level_moment_submission_by_query([peil, "student"])
            row = subplots.positions[peil]['row']
            col = subplots.positions[peil]['col']
            if l_level_moment is None:
                # nog niet ingevuld
                l_assignment = course.get_first_level_moment_by_query([peil, "student"])

                l_level_moment = Submission(0, 0, 0, 0,
                                            l_assignment.name, l_assignment.get_date(), l_assignment.get_day(),
                                            None, None,
                                            "1", False,
                                            None, None, None,
                                            -1, None, 3, 0)
            plot_overall_level_moment(row, col, fig, course, l_level_moment, level_serie_collection)

        for grade_moment in course.grade_moments.moments:
            # print("GP21 - Beordelingsmoment", grade_moment, "overall")
            l_grade_moment = student.get_grade_moment_submission_by_query([grade_moment, "student"])
            row = subplots.positions[grade_moment]['row']
            col = subplots.positions[grade_moment]['col']
            if l_grade_moment is None:
                # nog niet ingevuld
                l_assignment = course.get_first_grade_moment_by_query([grade_moment, "student"])
                l_grade_moment = Submission(0, 0, 0, 0,
                                            l_assignment.name, l_assignment.get_date(), l_assignment.get_day(),
                                            None, None,
                                            "1", False, None, None, None,
                                            -1, None, 3, 0)

            plot_overall_grade_moment(row, col, fig, course, l_grade_moment, level_serie_collection)
    student_name = student.email.split("@")[0].lower()
    file_name_html = instances.get_temp_path() + student_name + "_progress.html"
    file_name_jpg = instances.get_student_path() + student_name + "_progress.jpg"
    fig.write_html(file_name_html, include_plotlyjs="cdn")
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

    l_level_construction = level_construct(course)
    l_grade_construction = grade_construct(course)
    count = 0
    for student in results.students:
        l_level_construction = find_submissions(student, l_level_construction)
        l_grade_construction = find_submissions(student, l_grade_construction)
        # print(l_peil_construction)
        print("GPL90 -", student.name)

        plot_student(instance, course, student, results.actual_date, results.actual_day,
                     l_level_construction, l_grade_construction,
                     dashboard.subplot,
                     dashboard.level_serie_collection)

    print("GPL99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_plotly(sys.argv[1])
    else:
        generate_plotly("")

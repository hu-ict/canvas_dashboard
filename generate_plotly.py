import sys

from canvasapi import Canvas
from plotly.subplots import make_subplots

from lib.build_plotly_attendance import plot_attendance_perspective
from lib.build_plotly_perspective import plot_perspective, find_submissions, plot_overall_peilingen
from lib.lib_date import get_date_time_loc, get_actual_date, API_URL
from lib.file import read_course, read_results, read_course_instance, read_levels, read_levels_from_canvas, read_start
from lib.translation_table import translation_table
from model.Submission import Submission


def peil_construct(a_course):
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


def plot_student(instances, course, student, actual_date, actual_day, a_peil_construction, positions, subplot_titles, specs, level_serie_collection):
    if instances.is_instance_of('inno_courses'):
        fig = make_subplots(rows=2, cols=6, subplot_titles=subplot_titles, specs=specs, vertical_spacing=0.10,
                            horizontal_spacing=0.08)
    else:
        fig = make_subplots(rows=2, cols=6, subplot_titles=subplot_titles, specs=specs, vertical_spacing=0.10,
                            horizontal_spacing=0.08)

    fig.update_layout(height=900, width=1200, showlegend=False)
    for perspective in student.perspectives.values():
        row = positions[perspective.name]['row']
        col = positions[perspective.name]['col']
        plot_perspective(row, col, fig, course, perspective, a_peil_construction, actual_day, get_date_time_loc(actual_date), level_serie_collection)

    if course.attendance is not None:
        row = positions["attendance"]['row']
        col = positions["attendance"]['col']
        plot_attendance_perspective(row, col, fig, course, student.attendance_perspective, actual_day, get_date_time_loc(actual_date), level_serie_collection)

    if instances.is_instance_of('inno_courses'):
        # Peil overall drie peilmomenten
        for peil in course.level_moments.moments:
            # print("GP21 - Peilmoment", peil, "overall")
            level_moment = student.get_peilmoment_submission_by_query([peil, "overall"])
            if level_moment is None:
                # nog niet ingevuld
                l_assignment = course.get_first_level_moment_by_query([peil, "overall"])
                l_level_moment = Submission(0, 0, 0, 0, l_assignment.name, l_assignment.get_date(),
                                            l_assignment.get_day(),
                                            None, None, False, "1", None, None, -1, 3, 0)
                row = positions[peil]['row']
                col = positions[peil]['col']
                plot_overall_peilingen(row, col, fig, course, l_level_moment, level_serie_collection)
            else:
                # ingevuld
                row = positions[peil]['row']
                col = positions[peil]['col']
                plot_overall_peilingen(row, col, fig, course, level_moment, level_serie_collection)


    file_name = instances.get_student_path() + student.name + " progress"
    asci_file_name = file_name.translate(translation_table)
    fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
    fig.write_image(asci_file_name + ".jpeg")
    # if a_instances.current_instance == "sep24_inno":
    #     volg_nr = str(results.actual_day).zfill(3)
    #     file_name = "./time_lap/" + a_student.name + "_" + volg_nr + ".jpeg"
    #     asci_file_name = file_name.translate(translation_table)
    #     fig.write_image(asci_file_name)


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GP02 - Instance:", instances.current_instance)
    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    # level_serie_collection = read_levels("levels.json")
    start = read_start(instances.get_start_file_name())
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GR03 - Username", user.name)
    canvas_course = canvas.get_course(course.canvas_id)
    level_serie_collection = read_levels_from_canvas(canvas_course)

    if results.actual_day > course.days_in_semester:
        course.days_in_semester = results.actual_day + 1

    # Define bar properties

    subplot_titles = []
    for perspective in course.perspectives.values():
        subplot_titles.append(perspective.title)
    if instances.is_instance_of('prop_courses'):
        positions = {'kennis': {'row': 1, 'col': 1},
                     'verbreding': {'row': 1, 'col': 4},
                     'skills': {'row': 2, 'col': 1},
                     'attendance': {'row': 2, 'col': 4}
                     }
        specs = [
            [
                {'type': 'scatter', 'colspan': 3}, None, None, {'type': 'scatter', 'colspan': 3}, None, None
            ],
            [
                {'type': 'scatter', "colspan": 3}, None, None, {'type': 'scatter', "colspan": 3}, None, None
            ]
        ]
    elif instances.is_instance_of('inno_courses'):
        subplot_titles.append("Halfweg")
        subplot_titles.append("Sprint 7")
        subplot_titles.append("Eindbeoordeling")
        positions = {'team': {'row': 1, 'col': 1},
                     'gilde': {'row': 1, 'col': 4},
                     'kennis': {'row': 2, 'col': 1},
                     'Sprint 4': {'row': 2, 'col': 4},
                     'Sprint 7': {'row': 2, 'col': 5},
                     'Beoordeling': {'row': 2, 'col': 6}}
        specs = [
            [{'type': 'scatter', 'colspan': 3}, None, None, {'type': 'scatter', 'colspan': 3}, None, None],
            [{'type': 'scatter', "colspan": 3}, None, None, {'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        ]
    else:
        subplot_titles = ["Kennis", "Project"]
        positions = {'kennis': {'row': 1, 'col': 1},
                     'skills': {'row': 1, 'col': 4}
                     }
        specs = [
            [
                {'type': 'scatter', 'colspan': 3}, None, None, {'type': 'scatter', 'colspan': 3}, None, None
            ],
            [
                {'type': 'scatter', "colspan": 3}, None, None, {'type': 'scatter', "colspan": 3}, None, None
            ]
        ]
    peil_construction = peil_construct(course)
    count = 0
    for student in results.students:
        l_peil_construction = find_submissions(student, peil_construction)
        # print(l_peil_construction)
        print("GP90 -", student.name)

        plot_student(instances, course, student, results.actual_date, results.actual_day, l_peil_construction, positions,
                         subplot_titles, specs, level_serie_collection)

    print("GP99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GP01 - generate_plotly.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
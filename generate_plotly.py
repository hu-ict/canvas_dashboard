import sys

from plotly.subplots import make_subplots
from lib.build_plotly_perspective import plot_perspective, find_submissions, plot_overall_peilingen
from lib.lib_date import get_date_time_loc, get_actual_date
from lib.file import read_start, read_course, read_results, read_levels, read_course_instance
from lib.translation_table import translation_table
from model.Submission import Submission


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GP02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(start.course_file_name)
    results = read_results(start.results_file_name)
    levels = read_levels("levels.json")

    if results.actual_day > course.days_in_semester:
        course.days_in_semester = results.actual_day + 1

    # Define bar properties

    subplot_titles = []
    for perspective in course.perspectives.values():
        subplot_titles.append(perspective.title)
    if instances.is_instance_of('prop_courses'):
        positions = {'kennis': {'row': 1, 'col': 1},
                     'oriëntatie': {'row': 1, 'col': 4},
                     'PS en project': {'row': 2, 'col': 1},
                     'aanwezig': {'row': 2, 'col': 4}
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
        subplot_titles.append("Ná sprint 7")
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
                     'project': {'row': 1, 'col': 4}
                     }
        specs = [
            [
                {'type': 'scatter', 'colspan': 3}, None, None, {'type': 'scatter', 'colspan': 3}, None, None
            ],
            [
                {'type': 'scatter', "colspan": 3}, None, None, {'type': 'scatter', "colspan": 3}, None, None
            ]
        ]

    def peil_construct(a_course):
        l_peilingen = {}
        if a_course.level_moments is None or len(a_course.level_moments.assignment_groups) == 0:
            return l_peilingen
        for perspective in a_course.perspectives.values():
            l_peilingen[perspective.name] = []
        assignment_group = a_course.find_assignment_group(a_course.level_moments.assignment_groups[0])
        for assignment in assignment_group.assignments:
            #zoek de juiste Assignment
            for peil_label in a_course.level_moments.moments:
                if peil_label.lower() in assignment.name.lower():
                    #zoek het juiste Perspective
                    for perspective_name in l_peilingen:
                        if perspective_name.lower() in assignment.name.lower():
                            l_peilingen[perspective_name].append({'assignment': assignment, 'submission': None})
        return l_peilingen


    def plot_student(a_instances, a_start, a_course, a_student, a_actual_date, a_peil_construction):
        if instances.is_instance_of('inno_courses'):
            fig = make_subplots(rows=2, cols=6, subplot_titles=subplot_titles, specs=specs, vertical_spacing=0.10, horizontal_spacing=0.08)
        else:
            fig = make_subplots(rows=2, cols=6, subplot_titles=subplot_titles, specs=specs, vertical_spacing=0.10, horizontal_spacing=0.08)

        fig.update_layout(height=900, width=1200, showlegend=False)
        for perspective in a_student.perspectives.values():
            row = positions[perspective.name]['row']
            col = positions[perspective.name]['col']
            plot_perspective(row, col, fig, a_instances, a_start, a_course, perspective, a_peil_construction,
                              results.actual_day, get_date_time_loc(a_actual_date), levels)

        if a_instances.is_instance_of('inno_courses'):
            # Peil overall drie peilmomenten
            for peil in a_course.level_moments.moments[1:]:
                # print("GP21 - Peilmoment", peil, "overall")
                level_moment = a_student.get_peilmoment_submission_by_query([peil, "overall"])
                if level_moment is not None:
                    # ingevuld
                    plot_overall_peilingen(fig, positions[peil]['row'], positions[peil]['col'], a_start, a_course, level_moment, levels)
                else:
                    # nog niet ingevuld
                    l_assignment = a_course.get_level_moments_by_query([peil, "overall"])
                    l_level_moment = Submission(0, 0, 0, 0, l_assignment.name, l_assignment.assignment_date, l_assignment.assignment_day,
                                               None, None, False, None, None, -1, 3, 0)
                    plot_overall_peilingen(fig, positions[peil]['row'], positions[peil]['col'], a_start, a_course, l_level_moment, levels)

        file_name = a_instances.get_plot_path() + a_student.name
        asci_file_name = file_name.translate(translation_table)
        fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
        fig.write_image(asci_file_name + ".jpeg")
        if a_instances.current_instance == "feb24_inno":
            volg_nr = str(results.actual_day).zfill(3)
            file_name = "./time_lap/" + a_student.name + "_" + volg_nr + ".jpeg"
            asci_file_name = file_name.translate(translation_table)
            fig.write_image(asci_file_name)



    peil_construction = peil_construct(course)
    # print(peil_construction)
    # peil_construction = None

    count = 0
    for student in results.students:
        l_peil_construction = find_submissions(student, peil_construction)
        # print(l_peil_construction)
        print("GP90 -", student.name)
        plot_student(instances, start, course, student, results.actual_date, l_peil_construction)

    print("GP99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GP01 - generate_plotly.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
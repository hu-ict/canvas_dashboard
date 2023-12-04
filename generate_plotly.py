import math
import sys

import plotly.graph_objs as go
from plotly.subplots import make_subplots
from lib.build_plotly_perspective import plot_perspective, find_submissions
from lib.lib_date import get_date_time_loc, get_actual_date
from lib.lib_plotly import peil_labels, get_color_bar
from lib.file import read_start, read_course, read_results, read_labels_colors, read_course_instance
from lib.translation_table import translation_table


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    traces = []
    course = read_course(start.course_file_name)
    results = read_results(start.results_file_name)
    labels_colors = read_labels_colors("labels_colors.json")

    if results.actual_day > course.days_in_semester:
        course.days_in_semester = results.actual_day + 1

    bins_bar = [0, 0.9, 1.9, 2.9, 3.9, 4.9]
    # Define bar properties

    if instances.is_instance_of('prop_courses'):
        titles = ["Finals", "Toets", "Project", "Aanwezig"]
        positions = {'final': {'row': 1, 'col': 1},
                     'toets': {'row': 1, 'col': 4},
                     'project': {'row': 2, 'col': 1},
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
        titles = ["Team", "Kennis", "Gilde", "Halfweg", "Ná sprint 7", "Eindbeoordeling"]
        positions = {'team': {'row': 1, 'col': 1},
                     'gilde': {'row': 2, 'col': 1},
                     'kennis': {'row': 1, 'col': 4},
                     'halfweg': {'row': 2, 'col': 4},
                     'eind': {'row': 2, 'col': 5},
                     'beoordeling': {'row': 2, 'col': 6}}
        specs = [
            [
                {'type': 'scatter', 'colspan': 3}, None, None,
                {'type': 'scatter', 'colspan': 3}, None, None
            ],
            [
                {'type': 'scatter', "colspan": 3}, None, None, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}
            ]
        ]
    else:
        titles = ["Kennis", "Project"]
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


    def peil_construct(a_start, a_course):
        l_peilingen = {}
        if a_start.progress_perspective is None:
            return l_peilingen
        for perspective in a_course.perspectives.values():
            # peil is niet echt een perspective
            if perspective.name != a_start.progress_perspective:
                l_peilingen[perspective.name] = []
        progress_perspective = a_course.perspectives[a_start.progress_perspective]
        assignment_group = a_course.find_assignment_group(progress_perspective.assignment_groups[0])
        for assignment in assignment_group.assignments:
            #zoek de juiste Assignment
            for peil_label in peil_labels:
                if peil_label.lower() in assignment.name.lower():
                    #zoek het juiste Perspective
                    for perspective_name in l_peilingen:
                        if perspective_name.lower() in assignment.name.lower():
                            l_peilingen[perspective_name].append({'assignment': assignment, 'submission': None})
        return l_peilingen


    def plot_gauge(a_row, a_col, a_fig, a_peil, a_start, a_course, a_labels_colors):
        # plotting de gauge
        colors_bar = get_color_bar(a_start, a_course, a_labels_colors)
        plot_bgcolor = "#eee"
        quadrant_colors = list(colors_bar.values())[1:]
        n_quadrants = len(quadrant_colors)
        total_reference_moments = 4

        # deel de gauge op in n quadrants (met getallen die niet heel deelbaar zijn door n is het laatste quadrant
        # nu korter)
        gauge_quadrants = list(
            range(0, math.ceil(total_reference_moments + total_reference_moments / n_quadrants),
                  math.ceil(total_reference_moments / n_quadrants)))

        l_gauge = go.Indicator(
            mode="gauge",
            value=a_peil,

            delta={
                'reference': 0,
                'increasing': {
                    'color': quadrant_colors[[a_peil > x for x in gauge_quadrants].index(False) - 1],
                    'symbol': ''
                }
            },
            gauge={
                'axis': {
                    'visible': False,
                    'range': [None, total_reference_moments],
                    'dtick': math.ceil(total_reference_moments / n_quadrants)
                },

                'bar': {'color': "#555555", 'thickness': 0.3},
                'bgcolor': plot_bgcolor,
                'steps': [
                    {'line': {'width': 0}, 'range': [gauge_quadrants[i], gauge_quadrants[i + 1]],
                     'color': quadrant_colors[i]}
                    for i in range(len(gauge_quadrants) - 1)],
                'threshold': {
                    'line': {'color': "#555555", 'width': 12},
                    'thickness': 0.6,
                    'value': a_peil}})
        a_fig.add_trace(l_gauge, a_row, a_col)


    def plot_student(a_instances, a_start, a_course, a_student, a_actual_date, a_peil_construction):
        fig = make_subplots(rows=2, cols=6, subplot_titles=titles, specs=specs, vertical_spacing=0.15, horizontal_spacing=0.08)
        fig.update_layout(height=1000, width=1200, showlegend=False)
        for perspective in a_student.perspectives.values():
            if perspective.name != a_start.progress_perspective:
                row = positions[perspective.name]['row']
                col = positions[perspective.name]['col']
                plot_perspective(row, col, fig, a_instances, a_start, a_course, perspective, a_peil_construction,
                                 results.actual_day, get_date_time_loc(a_actual_date), labels_colors)

        if a_instances.is_instance_of('inno_courses'):
            # Peil overall drie peilmomenten
            if a_student.get_peilmoment(261031):
                plot_gauge(positions['halfweg']['row'], positions['halfweg']['col'], fig, a_student.get_peilmoment(261031).score + 0.5, a_start, a_course, labels_colors)
            else:
                plot_gauge(positions['halfweg']['row'], positions['halfweg']['col'], fig, 0.1, a_start, a_course, labels_colors)
            if a_student.get_peilmoment(252847):
                plot_gauge(positions['eind']['row'], positions['eind']['col'], fig, a_student.get_peilmoment(252847).score + 0.5, a_start, a_course, labels_colors)
            else:
                plot_gauge(positions['eind']['row'], positions['eind']['col'], fig, 0.1, a_start, a_course, labels_colors)
            if a_student.get_peilmoment(253129):
                plot_gauge(positions['beoordeling']['row'], positions['beoordeling']['col'], fig, a_student.get_peilmoment(253129).score + 0.5, a_start, a_course, labels_colors)
            else:
                plot_gauge(positions['beoordeling']['row'], positions['beoordeling']['col'], fig, 0.1, a_start, a_course, labels_colors)

        file_name = a_instances.get_plot_path() + a_student.name
        asci_file_name = file_name.translate(translation_table)
        fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
        fig.write_image(asci_file_name + ".jpeg")
        if a_instances.current_instance == "sep23_inno":
            volg_nr = str(results.actual_day).zfill(3)
            file_name = "./time_lap/" + a_student.name + "_" + volg_nr + ".jpeg"
            asci_file_name = file_name.translate(translation_table)
            fig.write_image(asci_file_name)


    # PROP
    peil_construction = peil_construct(start, course)
    # print(peil_construction)
    # peil_construction = None

    count = 0
    for student in results.students:
        l_peil_construction = find_submissions(student, peil_construction)
        # print(l_peil_construction)
        print(student.name)
        plot_student(instances, start, course, student, results.actual_date, l_peil_construction)

    print("Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
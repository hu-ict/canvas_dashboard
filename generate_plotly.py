import math
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from lib.build_plotly_perspective import plot_perspective, find_submissions
from lib.lib_date import get_date_time_loc
from lib.lib_plotly import peil_labels, score_dict, colors_bar, plot_path
from lib.file import read_start, read_course, read_results
from lib.translation_table import translation_table


print(score_dict['voortgang'][-1], score_dict['voortgang'][-1]['color'])
traces = []
start = read_start()
course = read_course(start.course_file_name)
results = read_results(start.results_file_name)
g_actual_day = (results.actual_date - start.start_date).days


bins_bar = [0, 0.9, 1.9, 2.9, 3.9, 4.9]
# Define bar properties
specs = [
            [
                {'type': 'scatter', 'colspan': 3, "rowspan": 2}, None, None, {'type': 'scatter', 'colspan': 3, "rowspan": 2}, None, None
            ],
            [
                None, None, None, None, None, None,
            ],
            [
                {'type': 'scatter', "colspan": 3, "rowspan": 2}, None, None, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}
            ],
            [
                None, None, None, None, None, None,
            ]
]

titles = ["Team", "Kennis", "Gilde", "Halfweg", "Ná sprint 7", "Beoordeling"]
positions = {'team': {'row': 1, 'col': 1},
             'gilde': {'row': 3, 'col': 1},
             'kennis': {'row': 1, 'col': 4},
             'halfweg': {'row': 3, 'col': 4},
             'eind': {'row': 3, 'col': 5},
             'beoordeling': {'row': 3, 'col': 6}}


def peil_contruct(a_course):
    l_peilingen = {}
    for perspective in a_course.perspectives:
        # peil is niet echt een perspective
        if perspective.name != 'peil':
            l_peilingen[perspective.name] = []
    peil_perspective = a_course.find_perspective_by_name(start.peil_perspective)
    assignment_group = a_course.find_assignment_group(peil_perspective.assignment_groups[0])
    for assignment in assignment_group.assignments:
        #zoek de juiste Assignment
        for peil_label in peil_labels:
            if peil_label.lower() in assignment.name.lower():
                #zoek het juiste Perspective
                for perspective_name in l_peilingen:
                    if perspective_name.lower() in assignment.name.lower():
                        l_peilingen[perspective_name].append({'assignment': assignment, 'submission': None})
    return l_peilingen


def plot_gauge(a_row, a_col, a_fig, a_peil):
    # plotting de gauge
    plot_bgcolor = "#fff"
    quadrant_colors = list(colors_bar.values())[1:]
    n_quadrants = len(quadrant_colors)
    total_reference_moments = 4

    # deel de gauge op in n quadrants (met getallen die niet heel deelbaar zijn door n is het laatste quadrant
    # nu korter)
    gauge_quadrants = list(
        range(0, math.ceil(total_reference_moments + total_reference_moments / n_quadrants),
              math.ceil(total_reference_moments / n_quadrants)))

    gauge = go.Indicator(
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
    a_fig.add_trace(gauge, a_row, a_col)


def plot_student(a_course, a_student, a_peil_construction):
    fig = make_subplots(rows=4, cols=6, subplot_titles=titles, specs=specs, vertical_spacing=0.15, horizontal_spacing=0.08)
    fig.update_layout(height=1000, width=1200, showlegend=False)
    for perspective in a_student.perspectives:
        if perspective.name in a_peil_construction:
            row = positions[perspective.name]['row']
            col = positions[perspective.name]['col']
            #slechts één assgignment_group
            assigment_group = a_course.find_assignment_group(perspective.assignment_groups[0])
            plot_perspective(row, col, fig, assigment_group, perspective, a_peil_construction,
                             start.start_date, g_actual_day, a_course.days_in_semester,
                             get_date_time_loc(results.actual_date))

    #Peil overall drie peilmomenten
    if a_student.get_peilmoment(247774):
        plot_gauge(positions['halfweg']['row'], positions['halfweg']['col'], fig,
                   a_student.get_peilmoment(247774).score + 0.5)
    else:
        plot_gauge(positions['halfweg']['row'], positions['halfweg']['col'], fig, 0.1)
    if a_student.get_peilmoment(252847):
        plot_gauge(positions['eind']['row'], positions['eind']['col'], fig,
                   a_student.get_peilmoment(252847).score + 0.5)
    else:
        plot_gauge(positions['eind']['row'], positions['eind']['col'], fig, 0.1)
    if a_student.get_peilmoment(253129):
        plot_gauge(positions['beoordeling']['row'], positions['beoordeling']['col'], fig,
                   a_student.get_peilmoment(253129).score + 0.5)
    else:
        plot_gauge(positions['beoordeling']['row'], positions['beoordeling']['col'], fig, 0.1)

    file_name = plot_path + a_student.name
    asci_file_name = file_name.translate(translation_table)
    fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
    fig.write_image(asci_file_name + ".jpeg")
    volg_nr = str(g_actual_day).zfill(3)
    file_name = "./time_lap/" + a_student.name + "_" + volg_nr + ".jpeg"
    asci_file_name = file_name.translate(translation_table)
    fig.write_image(asci_file_name)

peil_construction = peil_contruct(course)
for perspective in peil_construction:
    print("Perspective", perspective)
    for peil in peil_construction[perspective]:
        print("Peil", peil["assignment"].name, "Submission", peil["submission"])

count = 0
for student in results.students:
    l_peil_construction = find_submissions(student, peil_construction.copy())
    print(student.name)
    plot_student(course, student, l_peil_construction)


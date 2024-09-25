import plotly.graph_objects as go

from lib.lib_date import get_date_time_loc
from lib.translation_table import translation_table


# def build_portfolio_items(instances, course, student, levels):
#     # maak de kolommen
#     header_values = ["Portfolio-item", "Datum", "Status"]
#     table_values = [[], [], []]
#     # for learning_outcome in course.learning_outcomes:
#     #     header_values.append(learning_outcome.short)
#     #     table_values.append([])
#
#     column = 0
#     for perspective in course.perspectives.values():
#         for assignment_group_id in perspective.assignment_groups:
#             assignment_groep = course.find_assignment_group(assignment_group_id)
#             for assignment_sequence in assignment_groep.assignment_sequences:
#                 table_values[0].append(assignment_sequence.name + " ("+str(len(assignment_sequence.assignments))+")")
#                 table_values[1].append(get_date_time_loc(assignment_sequence.get_date()))
#                 table_values[2].append("Compleet")


    # fig = go.Figure(data=[go.Table(
    #     header=dict(values=header_values,
    #                 line_color='darkslategray',
    #                 fill_color='lightskyblue',
    #                 align='left'),
    #     cells=dict(values=table_values,
    #                line_color='darkslategray',
    #                fill_color='lightcyan',
    #                align='left'))
    # ])
    #
    # # fig.update_layout(width=1200, height=1200)
    # file_name = instances.get_plot_path() + student.name + " portfolio1"
    # asci_file_name = file_name.translate(translation_table)
    # fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
    # fig.write_image(asci_file_name + ".jpeg")

# def build_portfolio_items(instances, course, student, levels):
#     # maak de kolommen
#     header_values = ["Portfolio-item", "Datum", "Status"]
#     table_values = [[], [], []]
#     # for learning_outcome in course.learning_outcomes:
#     #     header_values.append(learning_outcome.short)
#     #     table_values.append([])
#
#     column = 0
#     for perspective in course.perspectives.values():
#         for assignment_group_id in perspective.assignment_groups:
#             assignment_groep = course.find_assignment_group(assignment_group_id)
#             for assignment_sequence in assignment_groep.assignment_sequences:
#                 table_values[0].append(assignment_sequence.name + " ("+str(len(assignment_sequence.assignments))+")")
#                 table_values[1].append(get_date_time_loc(assignment_sequence.get_date()))
#                 table_values[2].append("Compleet")


    # fig = go.Figure(data=[go.Table(
    #     header=dict(values=header_values,
    #                 line_color='darkslategray',
    #                 fill_color='lightskyblue',
    #                 align='left'),
    #     cells=dict(values=table_values,
    #                line_color='darkslategray',
    #                fill_color='lightcyan',
    #                align='left'))
    # ])
    #
    # # fig.update_layout(width=1200, height=1200)
    # file_name = instances.get_plot_path() + student.name + " portfolio1"
    # asci_file_name = file_name.translate(translation_table)
    # fig.write_html(asci_file_name + ".html", include_plotlyjs="cdn")
    # fig.write_image(asci_file_name + ".jpeg")

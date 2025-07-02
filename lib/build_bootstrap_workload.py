# Importeren plotly html in index html file
from lib.file import read_plotly
from lib.lib_date import get_date_time_loc


def build_workload_overtime(course, total_workload, templates):
    overtime_html_string = ""
    overtime_table = ""
    overtime_html_string += templates['workload_overtime'].substitute(
        {
            'overtime_table': overtime_table
        })
    return overtime_html_string


def build_workload_index(instance, course, total_workload, actual_date, templates):
    workload_tabs = {}
    if instance.is_instance_of("inno_courses"):
        workload_tabs['Over tijd'] = build_workload_overtime(course, total_workload, templates)


    file_name_html = instance.get_temp_path() + "_workload.html"
    workload_tabs['Werkvoorraad'] = '<h2 class="mt-2">Werkvoorraad</h2>' + read_plotly(file_name_html)
    # print("BSI10 - ", student_tabs.keys())
    workload_tabs_html_string = build_workload_tabs(instance, course, workload_tabs)
    workload_index_html_string = templates['workload_index'].substitute(
        {
            'semester': course.name,
            'actual_date': get_date_time_loc(actual_date),
            'student_tabs': workload_tabs_html_string
        }
    )
    file_name_html = instance.get_html_path() + "workload_index.html"
    # print("BB21 - Write portfolio for", student.name)
    with open(file_name_html, mode='w', encoding="utf-8") as file_portfolio:
        file_portfolio.write(workload_index_html_string)
    return

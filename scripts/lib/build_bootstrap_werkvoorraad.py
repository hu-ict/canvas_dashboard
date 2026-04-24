from scripts.lib.file import read_plotly

WORKLOAD_PLOTLY = "workload_plotly"
WORKLOAD_INDEX = "workload_index"

def build_bootstrap_workload_tab(a_instance, a_templates, a_workload):
    overzicht_html_string = ""
    for dimension in a_workload.dimensions:
        list_html_string = ""
        dimension_link_path_name = a_instance.get_link_general_path() + WORKLOAD_PLOTLY + "_" + dimension.name + ".html"
        for item in dimension.items:
            item_file_name = dimension.name + "_" + item.short + ".html"
            link_path_name = a_instance.get_link_general_path() + item_file_name
            list_html_string += a_templates["selector"].substitute(
                    {'selector_file': link_path_name, 'selector_name': item.name,  'selector': item.short})
        overzicht_html_string += a_templates["overzicht"].substitute({'url': dimension_link_path_name, 'perspective': dimension.description, 'buttons': list_html_string})
    return overzicht_html_string


def build_workload_index_html(a_instance, a_course, a_workload, a_actual_date, a_templates):
    for dimension in a_workload.dimensions:
        html_string = ""
        file_name = a_instance.get_html_general_path() + WORKLOAD_PLOTLY + "_" + dimension.name + ".html"
        html_string += a_templates["workload_index"].substitute(
            {'semester': a_course.name,
             'actual_date': a_actual_date,
             'workload_plot': read_plotly(file_name),
             'workload_late': build_workload_dimension_overview(dimension, a_templates)})
        file_name_html = a_instance.get_html_general_path() + WORKLOAD_INDEX + "_" + dimension.name + ".html"
        # print("BB21 - Write portfolio for", student.name)
        with open(file_name_html, mode='w', encoding="utf-8") as file:
            file.write(html_string)


def build_workload_dimension_overview(workload_dimension, templates):
    problem_html = ""
    problem_count = 0
    for item in workload_dimension.items:
        if item.w2_count > 0 or item.w3_count > 0:
            problem_html += templates["workload_problem"].substitute({'url': 'url',
                            'assessor': item.name,
                            'items_open': item.w1_count+item.w2_count+item.w3_count,
                            'items_late': item.w2_count+item.w3_count,
                            'items_to_late': item.w3_count,
                            'items_problem': problem_count
                            })
    html_string = templates["workload_problems"].substitute({'problems': problem_html})
    return html_string


# def workload_email(recipients, recipients_cc, html_message):
#     html_body = "Beste INNO-docenten<br><br>Hierbij de gevraagde uitdraai en reminder:<br><br>"
#     html_body += html_message
#     html_body += "<br>Ga naar het INNO-dashboard en navigeer naar werkvoorraad en klik links op je initialen. Je krijgt nu een actueel overzicht van openstaande opleveringen.<br><br>Groet Berend"
#     outlook = client.Dispatch('Outlook.Application')
#     message = outlook.CreateItem(0)
#     message.To = recipients
#     message.CC = recipients_cc
# #    message.Attachments.Add(file) # You can attach a file with this
#     message.Subject = 'INNO - Werkvoorraad reminder'
#     message.HTMLBody = html_body
#     message.Display()


def build_late_email(a_total_workload):
    for perspective in a_total_workload['perspectives'].keys():
        selectors = a_total_workload['perspectives'][perspective]['late']
        for selector in selectors:
            late_count = a_total_workload['perspectives'][perspective]['late'][selector]
            to_late_count = a_total_workload['perspectives'][perspective]['to_late'][selector]
            if late_count > 0 or to_late_count > 0:
                print(f"Voor {selector} {perspective} zijn {late_count+to_late_count} items een week te laat, daarvan staan {to_late_count} items langer dan 2 weken open")


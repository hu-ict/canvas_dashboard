from lib.file import read_plotly
import win32com.client as client


def build_bootstrap_teacher_tab(a_instance, a_templates, a_workload):
    overzicht_html_string = ""
    list_html_string = ""
    for teacher in a_workload.workload_teachers:
        list_html_string += a_templates["selector"].substitute(
                {'selector_file': ".//" + a_instance.name + "//general//teacher_" + teacher.initials + ".html", 'selector_name': teacher.name,  'selector': teacher.initials})

    overzicht_html_string += a_templates["overzicht"].substitute({'perspective': "Docent", 'buttons': list_html_string})
    return overzicht_html_string


def build_bootstrap_canvas_workload_general(a_instance, a_course, a_workload, a_actual_date, a_templates):
    html_string = ""
    file_name = a_instance.get_html_path() + "totals_werkvoorraad.html"
    html_string += a_templates["workload_index"].substitute(
        {'semester': a_course.name,
         'actual_date': a_actual_date,
         'workload_plot': read_plotly(file_name),
         'workload_late': build_problems(a_course, a_workload, a_templates)})
    file_name_html = a_instance.get_html_path() + "workload_index.html"
    # print("BB21 - Write portfolio for", student.name)
    with open(file_name_html, mode='w', encoding="utf-8") as file:
        file.write(html_string)


def build_problems(a_course, a_workload, a_templates):
    problem_html = ""
    problem_count = 0
    recipients = ""
    for teacher in a_workload.workload_teachers:
        if teacher.w2_count > 0 or teacher.w3_count > 0:
            problem_html += a_templates["workload_problem"].substitute({'url': 'url',
                            'assessor': teacher.name,
                            'items_open': teacher.w1_count+teacher.w2_count+teacher.w3_count,
                            'items_late': teacher.w2_count+teacher.w3_count,
                            'items_to_late': teacher.w3_count,
                            'items_problem': problem_count
                            })
    html_string = a_templates["workload_problems"].substitute({'problems': problem_html})
    return html_string


def workload_email(recipients, recipients_cc, html_message):
    html_body = "Beste INNO-docenten<br><br>Hierbij de gevraagde uitdraai en reminder:<br><br>"
    html_body += html_message
    html_body += "<br>Ga naar het INNO-dashboard en navigeer naar werkvoorraad en klik links op je initialen. Je krijgt nu een actueel overzicht van openstaande opleveringen.<br><br>Groet Berend"
    outlook = client.Dispatch('Outlook.Application')
    message = outlook.CreateItem(0)
    message.To = recipients
    message.CC = recipients_cc
#    message.Attachments.Add(file) # You can attach a file with this
    message.Subject = 'INNO - Werkvoorraad reminder'
    message.HTMLBody = html_body
    message.Display()


def build_late_email(a_total_workload):
    for perspective in a_total_workload['perspectives'].keys():
        selectors = a_total_workload['perspectives'][perspective]['late']
        for selector in selectors:
            late_count = a_total_workload['perspectives'][perspective]['late'][selector]
            to_late_count = a_total_workload['perspectives'][perspective]['to_late'][selector]
            if late_count > 0 or to_late_count > 0:
                print(f"Voor {selector} {perspective} zijn {late_count+to_late_count} items een week te laat, daarvan staan {to_late_count} items langer dan 2 weken open")


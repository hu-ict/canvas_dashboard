from lib.file import read_plotly
import win32com.client as client


def build_bootstrap_canvas_werkvoorraad_tab(a_instance, a_templates, a_course, a_perspectives, a_total_workload):
    overzicht_html_string = ""
    dict_index = 0
    for perspective in a_perspectives:
        if dict_index == 0 and a_instance.is_instance_of("prop_courses"):
            list_html_string = ""
            for selector in a_total_workload["perspectives"][perspective.name]["list"].keys():
                # print(selector)
                list_html_string += a_templates["selector"].substitute(
                    {'selector_file': ".//" + a_instance.name + "//general//late_" + selector + ".html", 'selector': selector})
            overzicht_html_string += a_templates["overzicht"].substitute({'perspective': "Totaal", 'buttons': list_html_string})

        list_html_string = ""
        for selector in a_total_workload["perspectives"][perspective.name]["list"].keys():
            # print(selector)
            list_html_string += a_templates["selector"].substitute(
                {'selector_file': ".//" + a_instance.name + "//general//late_" + perspective.name + "_" + selector + ".html", 'selector': selector})
        overzicht_html_string += a_templates["overzicht"].substitute(
            {'perspective': perspective.title, 'buttons': list_html_string})
        dict_index += 1
    return overzicht_html_string


def build_bootstrap_canvas_werkvoorraad_index(a_instance, a_course, a_actual_date, a_templates, a_total_workload):
    html_string = ""
    file_name = a_instance.get_html_path() + "totals_werkvoorraad.html"
    html_string += a_templates["workload_index"].substitute(
        {'semester': a_course.name,
         'actual_date': a_actual_date,
         'workload_plot': read_plotly(file_name),
         'workload_late': build_problems(a_course, a_templates, a_total_workload)})
    file_name_html = a_instance.get_html_path() + "workload_index.html"
    # print("BB21 - Write portfolio for", student.name)
    with open(file_name_html, mode='w', encoding="utf-8") as file_portfolio:
        file_portfolio.write(html_string)


def build_problems(a_course, a_templates, a_total_workload):
    problem_html = ""
    problem_count = 0
    recipients = ""
    for perspective in a_total_workload['perspectives'].keys():
        selectors = a_total_workload['perspectives'][perspective]['late']
        for selector in selectors:
            late_count = a_total_workload['perspectives'][perspective]['late'][selector]
            to_late_count = a_total_workload['perspectives'][perspective]['to_late'][selector]
            if late_count > 0 or to_late_count > 0:
                teacher =  a_course.find_teacher_by_initials(selector)
                if teacher is not None:
                    recipients += teacher.email + ";"
                    selector = teacher.name

                problem_html += a_templates["workload_problem"].substitute({'url': 'url',
                                                                            'selector': selector,
                                                                            'items_late': late_count+to_late_count,
                                                                            'items_to_late': to_late_count,
                                                                            'items_problem': problem_count
                                                                            })
    html_string = a_templates["workload_problems"].substitute({'problems': problem_html})
    recipients_cc = "karin.elich@hu.nl"
    workload_email(recipients, recipients_cc, html_string)
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

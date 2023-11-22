from operator import itemgetter
from string import Template

from lib.lib_date import get_date_time_loc, get_date_time_obj
from lib.file import template_path, html_path


def build_late(a_result, a_student_totals):
    for l_perspective in a_student_totals['perspectives'].keys():
        for l_selector in a_student_totals['perspectives'][l_perspective]['list'].keys():
            # print(l_selector)
            late_list = sorted(a_student_totals['perspectives'][l_perspective]['list'][l_selector], key=itemgetter('submitted_date'))
            # with open("late_"+l_perspective+"_"+l_selector+".json", 'w') as f:
            #     json.dump(late_list, f, indent=2)

    with open(template_path+'template_late.html', mode='r', encoding="utf-8") as file_late_template:
        string_late_html = file_late_template.read()
        late_html_template = Template(string_late_html)

    with open(template_path+'template_late_list.html', mode='r', encoding="utf-8") as file_late_list_template:
        string_late_list_html = file_late_list_template.read()
        late_list_html_template = Template(string_late_list_html)

    with open(template_path+'template_submission.html', mode='r', encoding="utf-8") as file_submission_template:
        string_submission_html = file_submission_template.read()
        submission_html_template = Template(string_submission_html)

    with open(template_path+'template_selector.html', mode='r', encoding="utf-8") as file_selector_template:
        string_selector_html = file_selector_template.read()
        selector_html_template = Template(string_selector_html)

    team_html_string = ""
    for selector in a_student_totals['perspectives']["team"]['list'].keys():
        # print(selector)
        team_html_string += selector_html_template.substitute(
            {'selector_file': "late_"+"team"+"_"+selector+".html", 'selector': selector})

    gilde_html_string = ""
    for selector in a_student_totals['perspectives']["gilde"]['list'].keys():
        gilde_html_string += selector_html_template.substitute(
            {'selector_file': "late_"+"gilde"+"_"+selector+".html", 'selector': selector})

    kennis_html_string = ""
    for selector in a_student_totals['perspectives']["kennis"]['list'].keys():
        kennis_html_string += selector_html_template.substitute(
            {'selector_file': "late_"+"kennis"+"_"+selector+".html", 'selector': selector})

    late_html_string = late_html_template.substitute({'team_buttons': team_html_string, 'gilde_buttons': gilde_html_string, 'kennis_buttons': kennis_html_string})

    with open(html_path+'late.html', mode='w', encoding="utf-8") as file_late:
        file_late.write(late_html_string)

    for l_perspective in a_student_totals['perspectives'].keys():
        # print(perspective)
        for l_selector in a_student_totals['perspectives'][l_perspective]['list']:
            late_list_temp = a_student_totals['perspectives'][l_perspective]['list'][l_selector]
            late_list = sorted(late_list_temp, key=itemgetter('submitted_date'))
            late_list_html_total_string = ''
            for l_submission in late_list:
                l_student_name = a_result.find_student(l_submission['student_id']).name
                url = "https://canvas.hu.nl/courses/"+str(a_result.id)+"/gradebook/speed_grader?assignment_id="+str(l_submission['assignment_id'])+"&student_id="+str(l_submission['student_id'])
                submission_html_string = submission_html_template.substitute({'submission_id': l_submission['id'], 'student_name': l_student_name, 'assignment_name': l_submission['assignment_name'], 'submission_date': get_date_time_loc(get_date_time_obj(l_submission['submitted_date'])), 'url': url})
                late_list_html_total_string += submission_html_string
            late_list_html_string = late_list_html_template.substitute({'submissions': late_list_html_total_string})
            with open(html_path+"late_"+l_perspective+"_"+l_selector+".html", mode='w', encoding="utf-8") as file_late_list:
                file_late_list.write(late_list_html_string)

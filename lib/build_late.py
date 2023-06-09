from operator import itemgetter
from string import Template

from lib.config import template_path, get_date_time_loc, get_date_time_obj


def build_late(a_course_id, a_submissions_late):
    for l_perspective in a_submissions_late.keys():
    # print(l_perspective)
        for l_selector in a_submissions_late[l_perspective].keys():
            # print(l_selector)
            late_list = sorted(a_submissions_late[l_perspective][l_selector], key=itemgetter('submitted_at'))
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
    for selector in a_submissions_late["team"].keys():
        # print(selector)
        team_html_string += selector_html_template.substitute(
            {'selector_file': "late_"+"team"+"_"+selector+".html", 'selector': selector})

    gilde_html_string = ""
    for selector in a_submissions_late["gilde"].keys():
        gilde_html_string += selector_html_template.substitute(
            {'selector_file': "late_"+"gilde"+"_"+selector+".html", 'selector': selector})

    kennis_html_string = ""
    for selector in a_submissions_late["kennis"].keys():
        kennis_html_string += selector_html_template.substitute(
            {'selector_file': "late_"+"kennis"+"_"+selector+".html", 'selector': selector})

    late_html_string = late_html_template.substitute({'team_buttons': team_html_string, 'gilde_buttons': gilde_html_string, 'kennis_buttons': kennis_html_string})

    with open(template_path+'late.html', mode='w', encoding="utf-8") as file_late:
        file_late.write(late_html_string)

    for l_perspective in a_submissions_late.keys():
        # print(perspective)
        for l_selector in a_submissions_late[l_perspective]:
            late_list_temp = a_submissions_late[l_perspective][l_selector]
            late_list = sorted(late_list_temp, key=itemgetter('submitted_at'))
            late_list_html_total_string = ''
            for late in late_list:
                url = "https://canvas.hu.nl/courses/"+str(a_course_id)+"/gradebook/speed_grader?assignment_id="+str(late['assignment_id'])+"&student_id="+str(late['student_id'])
                submission_html_string = submission_html_template.substitute({'submission_id': late['assignment_id'], 'assignment_name': late['assignment_name'], 'submission_date': get_date_time_loc(get_date_time_obj(late['submitted_at'])), 'url': url})
                late_list_html_total_string += submission_html_string
            late_list_html_string = late_list_html_template.substitute({'submissions': late_list_html_total_string})
            with open(template_path+"late_"+l_perspective+"_"+l_selector+".html", mode='w', encoding="utf-8") as file_late_list:
                file_late_list.write(late_list_html_string)

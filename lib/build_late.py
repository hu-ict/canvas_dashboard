import json
from operator import itemgetter
from string import Template
from lib.lib_date import get_date_time_loc, get_date_time_obj


def build_late_list(a_instances, a_start, a_result, a_student_totals):
    for perspective in a_student_totals['perspectives'].keys():
        for selector in a_student_totals['perspectives'][perspective]['list'].keys():
            # print(l_selector)
            late_list = sorted(a_student_totals['perspectives'][perspective]['list'][selector], key=itemgetter('submitted_date'))
            # with open("late_"+l_perspective+"_"+l_selector+".json", 'w') as f:
            #     json.dump(late_list, f, indent=2)

    with open(a_start.template_path+'template_late.html', mode='r', encoding="utf-8") as file_late_template:
        string_late_html = file_late_template.read()
        late_html_template = Template(string_late_html)

    with open(a_start.template_path+'template_late_perspective.html', mode='r', encoding="utf-8") as file_late_perspective_template:
        string_late_perspective_html = file_late_perspective_template.read()
        late_perspective_html_template = Template(string_late_perspective_html)

    with open(a_start.template_path+'template_late_list.html', mode='r', encoding="utf-8") as file_late_list_template:
        string_late_list_html = file_late_list_template.read()
        late_list_html_template = Template(string_late_list_html)

    with open(a_start.template_path+'template_submission.html', mode='r', encoding="utf-8") as file_submission_template:
        string_submission_html = file_submission_template.read()
        submission_html_template = Template(string_submission_html)

    with open(a_start.template_path+'template_selector.html', mode='r', encoding="utf-8") as file_selector_template:
        string_selector_html = file_selector_template.read()
        selector_html_template = Template(string_selector_html)

    all_late_substitute = ""
    file_list = ["late.html"]
    for perspective in a_student_totals['perspectives'].keys():
        late_substitute = ""
        for selector in a_student_totals['perspectives'][perspective]['list'].keys():
            # print("BL11 -", perspective, selector)
            file_name = "late_"+perspective+"_"+selector+".html"
            file_list.append(file_name)
            late_substitute += selector_html_template.substitute({'selector_file': file_name, 'selector': selector})
        all_late_substitute += late_perspective_html_template.substitute({"perspective": perspective, "buttons": late_substitute})
    late_html_string = late_html_template.substitute({"perspectives": all_late_substitute})

    with open(a_instances.get_project_path()+'file_list.json', 'w') as f:
        dict_result = file_list
        json.dump(dict_result, f, indent=2)

    with open(a_instances.get_html_path()+'late.html', mode='w', encoding="utf-8") as file_late:
        file_late.write(late_html_string)

    for perspective in a_student_totals['perspectives'].keys():
        # print(perspective)
        for selector in a_student_totals['perspectives'][perspective]['list']:
            # print("BL21 -", perspective, selector)
            late_list_temp = a_student_totals['perspectives'][perspective]['list'][selector]
            late_list = sorted(late_list_temp, key=itemgetter('submitted_date'))
            late_list_html_total_string = ''
            for l_submission in late_list:
                l_student_name = a_result.find_student(l_submission['student_id']).name
                url = "https://canvas.hu.nl/courses/"+str(a_result.id)+"/gradebook/speed_grader?assignment_id="+str(l_submission['assignment_id'])+"&student_id="+str(l_submission['student_id'])
                submission_html_string = submission_html_template.substitute({'submission_id': l_submission['id'], 'student_name': l_student_name, 'assignment_name': l_submission['assignment_name'], 'submission_date': get_date_time_loc(get_date_time_obj(l_submission['submitted_date'])), 'url': url})
                late_list_html_total_string += submission_html_string
            late_list_html_string = late_list_html_template.substitute({'submissions': late_list_html_total_string})
            file_name = "late_"+perspective+"_"+selector+".html"
            with open(a_instances.get_html_path()+file_name, mode='w', encoding="utf-8") as file_late_list:
                file_late_list.write(late_list_html_string)

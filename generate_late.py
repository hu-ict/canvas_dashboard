from string import Template

from generate_dashboard import template_path
from lib.file import read_late_json, read_course_config_start

structure = {
    'team': ['BW', 'MB', 'KE', 'TPM', 'PVR', 'MVD', 'HVG'],
    'gilde': ['AI', 'BIM', 'CSC', 'SD_B', 'SD_F', 'TI'],
    'kennis': ['AI', 'BIM', 'CSC', 'SD_B', 'SD_F', 'TI']
}

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

course_config_start = read_course_config_start()

team_html_string = ""
for selector in structure["team"]:
    print(selector)
    team_html_string += selector_html_template.substitute(
        {'selector_file': "late_"+"team"+"_"+selector+".html", 'selector': selector})

gilde_html_string = ""
for selector in structure["gilde"]:
    print(selector)
    gilde_html_string += selector_html_template.substitute(
        {'selector_file': "late_"+"gilde"+"_"+selector+".html", 'selector': selector})

kennis_html_string = ""
for selector in structure["kennis"]:
    print(selector)
    kennis_html_string += selector_html_template.substitute(
        {'selector_file': "late_"+"kennis"+"_"+selector+".html", 'selector': selector})

late_html_string = late_html_template.substitute({'team_buttons': team_html_string, 'gilde_buttons': gilde_html_string, 'kennis_buttons': kennis_html_string})

with open(template_path+'late.html', mode='w', encoding="utf-8") as file_late:
    file_late.write(late_html_string)

for perspective in structure.keys():
    print(perspective)
    for selector in structure[perspective]:
        print(selector)

        late_list = read_late_json("late_"+perspective+"_"+selector+".json")
        late_list_html_total_string = ''
        for late in late_list:
            url = "https://canvas.hu.nl/courses/"+str(course_config_start.course_id)+"/gradebook/speed_grader?assignment_id="+str(late.assignment_id)+"&student_id="+str(late.student_id)
            submission_html_string = submission_html_template.substitute({'submission_id': late.id, 'assignment_name': late.assignment_name, 'submission_date': late.submitted_at, 'url': url})
            late_list_html_total_string += submission_html_string
        late_list_html_string = late_list_html_template.substitute({'submissions': late_list_html_total_string})
        with open(template_path+"late_"+perspective+"_"+selector+".html", mode='w', encoding="utf-8") as file_late_list:
            file_late_list.write(late_list_html_string)


late_list_html_string = ''
# for late in late_list:
#     url = "https://canvas.hu.nl/courses/"+str(course_config_start.course_id)+"/gradebook/speed_grader?assignment_id="+str(late.assignment_id)+"&student_id="+str(late.student_id)
#     late_html_string = submission_html_template.substitute({'submission_id': late.id, 'assignment_name': late.assignment_name, 'submission_date': late.submitted_at, 'url': url})
#     late_list_html_string += late_html_string


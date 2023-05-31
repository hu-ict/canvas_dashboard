from string import Template

from generate_dashboard import template_path
from lib.file import read_late_json, read_course_config_start

with open(template_path+'template_late.html', mode='r', encoding="utf-8") as file_late_template:
    string_late_html = file_late_template.read()
    late_html_template = Template(string_late_html)

with open(template_path+'template_submission.html', mode='r', encoding="utf-8") as file_submission_template:
    string_submission_html = file_submission_template.read()
    submission_html_template = Template(string_submission_html)

course_config_start = read_course_config_start()

late_list = read_late_json()
late_list_html_string = ''
for late in late_list:
    url = "https://canvas.hu.nl/courses/"+str(course_config_start.course_id)+"/gradebook/speed_grader?assignment_id="+str(late.assignment_id)+"&student_id="+str(late.student_id)
    late_html_string = submission_html_template.substitute({'submission_id': late.id, 'assignment_name': late.assignment_name, 'submission_date': late.submitted_at, 'url': url})
    late_list_html_string += late_html_string

late_html_string = late_html_template.substitute({'submissions': late_list_html_string})

with open(template_path+'late.html', mode='w', encoding="utf-8") as file_late:
    file_late.write(late_html_string)

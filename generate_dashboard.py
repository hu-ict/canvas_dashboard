import json

from lib.file import read_late_json, read_course_config
from model.Statistics import Statistics
from model.Student import *
from model.StudentGroup import StudentGroup
from datetime import datetime
from string import Template

from translation_table import translation_table

start_date = datetime.strptime('06-02-23', '%d-%m-%y')
end_date = datetime.strptime('26-06-23', '%d-%m-%y')

# datetime object containing current date and time
actual_date = datetime.now()
timedelta = end_date - start_date
days_in_semester= timedelta.days
print("days_in_semester", days_in_semester)
days_per_sprint = days_in_semester // 16
semester_day = (actual_date - start_date).days
students = []
plot_path = "./dashboard - lokaal/plotly/"
template_path = "./dashboard - lokaal/"
index_path = template_path

course_config = read_course_config("course_config.json")

btn_colors = {
        "AI": "btn-warning",
        "BIM": "btn-success",
        "CSC": "btn-danger",
        "SD_B": "btn-dark",
        "SD_F": "btn-primary",
        "TI": "btn-info"
    }

studentGroups = []
aantal_studenten = 0

# Opening JSON file
f = open('student_results.json')
data = json.load(f)
actual_date = data['actual_date']
course_name = data['name']
statistics = Statistics.from_dict(data['statistics'])
for student_group_json in data['student_groups']:
    studentGroup = StudentGroup.from_dict(student_group_json)
    studentGroup.coach = course_config.find_student_group(studentGroup.id).coach
    print(studentGroup)
    for student_json in student_group_json['students']:
        student = Student.from_dict(student_json)
        studentGroup.students.append(student)
        aantal_studenten += 1
    studentGroups.append(studentGroup)

# Closing file
f.close()

# Het Bootstrap dashboard wordt hier opgebouwd

# Create a template that has placeholder for value of x
with open(template_path+'template.html', mode='r', encoding="utf-8") as file_index_template:
    string_index_html = file_index_template.read()
    index_html_template = Template(string_index_html)

with open(template_path+'studentgroup.html', mode='r', encoding="utf-8") as file_group_template:
    string_group_html = file_group_template.read()
    group_html_template = Template(string_group_html)

with open(template_path+'student.html', mode='r', encoding="utf-8") as file_student_template:
    string_student_html = file_student_template.read()
    student_html_template = Template(string_student_html)

# Substitute value of x in above template

groups_html_string = ''
for studentGroup in studentGroups:
    students_html_string = ''
    for student in studentGroup.students:
        role = student.get_role()
        color = btn_colors[role]
        file_name = "./plotly/" + student.name.replace(" ", "%20") + ".html"
#       file_name = plot_path + student.name + ".html"
        asci_file_name = file_name.translate(translation_table)
        student_role = course_config.find_role(student.roles)
        student_html_string = student_html_template.substitute({'btn_color': color, 'student_name': student.name, 'student_role': student_role.description, 'student_file': asci_file_name})
        students_html_string += student_html_string
    coach = studentGroup.coach.replace(' ', '_')
    group_html_string = group_html_template.substitute({'coach': coach, 'student_group_name': studentGroup.name, 'students': students_html_string})
    groups_html_string += group_html_string

index_html_string = index_html_template.substitute({'course_name' : course_name, 'aantal_studenten': aantal_studenten, 'aantal_teams': len(studentGroups),
                                                    'submission_count': statistics.submission_count, 'not_graded_count': statistics.not_graded_count,
                                                    'actual_date': actual_date, 'semester_day': semester_day, 'percentage': str(semester_day/1.5)+"%" , 'student_groups': groups_html_string})

with open(index_path+'index.html', mode='w', encoding="utf-8") as file_index:
    file_index.write(index_html_string)

# Het TO LATE scherm wordt hier opgebouwd

with open(template_path+'template_late.html', mode='r', encoding="utf-8") as file_late_template:
    string_late_html = file_late_template.read()
    late_html_template = Template(string_late_html)

with open(template_path+'template_submission.html', mode='r', encoding="utf-8") as file_submission_template:
    string_submission_html = file_submission_template.read()
    submission_html_template = Template(string_submission_html)

late_list = read_late_json()
late_list_html_string = ''
for late in late_list:
    url = "https://canvas.hu.nl/courses/32666/gradebook/speed_grader?assignment_id="+str(late.assignment_id)+"&student_id="+str(late.student_id)
    late_html_string = submission_html_template.substitute({'submission_id': late.id, 'assignment_name': late.assignment_name, 'submission_date': late.submitted_at, 'url': url})
    late_list_html_string += late_html_string

late_html_string = late_html_template.substitute({'submissions' : late_list_html_string})

with open(index_path+'late.html', mode='w', encoding="utf-8") as file_late:
    file_late.write(late_html_string)

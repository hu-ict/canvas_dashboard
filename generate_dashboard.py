from lib.file import read_late_json, read_course, read_course_config_start, read_results
from lib.translation_table import translation_table
from string import Template

course_config_start = read_course_config_start()
course = read_course(course_config_start.course_file_name)
results = read_results(course_config_start.results_file_name)

days_in_semester = (course_config_start.end_date - course_config_start.start_date).days
semester_day = (results.actual_date - course_config_start.start_date).days
print("Day in semester", semester_day, days_in_semester)
plot_path = "./dashboard - lokaal/plotly/"
template_path = "./dashboard - lokaal/"
index_path = template_path

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

with open(template_path+'coach.html', mode='r', encoding="utf-8") as file_coach_template:
    string_coach_html = file_coach_template.read()
    coach_html_template = Template(string_coach_html)

# Substitute value of x in above template
submission_count = 0
not_graded_count = 0
student_count = 0

coaches = {}
groups_html_string = ''
for group in results.studentGroups:
    students_html_string = ''
    if len(group.teachers) > 0:
        teacher_id = group.teachers[0]
        teacher = course.find_teacher(teacher_id)
        coaches[teacher.id] = teacher
    else:
        teacher = "Leeg"
    for student in group.students:
        student_count += 1
        role = student.get_role()
        role_obj = course.get_role(role)
        color = role_obj.btn_color
        file_name = "./plotly/" + student.name.replace(" ", "%20") + ".html"
        #       file_name = plot_path + student.name + ".html"
        asci_file_name = file_name.translate(translation_table)
        student_html_string = student_html_template.substitute(
            {'btn_color': color, 'student_name': student.name, 'student_role': role_obj.name,
             'student_file': asci_file_name})
        students_html_string += student_html_string

        for perspective in student.perspectives:
            for submission in perspective.submissions:
                submission_count += 1
                if not submission.graded:
                    not_graded_count += 1

    group_html_string = group_html_template.substitute({'coach': teacher.initials, 'student_group_name': group.name, 'students': students_html_string})
    groups_html_string += group_html_string


def get_initials(item):
    return item[1].initials


coaches = dict(sorted(coaches.items(), key=lambda item: get_initials(item)))

coaches_html_string = ''
for coach in coaches.values():
    coaches_html_string += coach_html_template.substitute({'coach_name': coach.name, 'coach_initials': coach.initials})

actual_date_str = results.actual_date.strftime("%d-%m-%Y %H:%M")
index_html_string = index_html_template.substitute({'course_name': course.name, 'aantal_studenten': student_count, 'aantal_teams': len(results.studentGroups),
                                                    'submission_count': submission_count, 'not_graded_count': not_graded_count,
                                                    'actual_date': actual_date_str, 'semester_day': semester_day,
                                                    'percentage': str(semester_day/1.5)+"%",
                                                    'coaches': coaches_html_string,
                                                    'student_groups': groups_html_string})

with open(index_path+'index.html', mode='w', encoding="utf-8") as file_index:
    file_index.write(index_html_string)

with open(template_path+'template_late.html', mode='r', encoding="utf-8") as file_late_template:
    string_late_html = file_late_template.read()
    late_html_template = Template(string_late_html)

with open(template_path+'template_submission.html', mode='r', encoding="utf-8") as file_submission_template:
    string_submission_html = file_submission_template.read()
    submission_html_template = Template(string_submission_html)

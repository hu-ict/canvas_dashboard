import json
from canvasapi import Canvas
from lib.config import API_URL, actual_date, DATE_TIME_STR
from lib.file import read_start, read_config
from model.Course import Course
from model.Perspective import Perspective
from model.Student import Student

course_config_start = read_start()
config = read_config(course_config_start.config_file_name)
print(config)

for teacher in config.teachers:
    for studentGroupId in teacher.projects:
        studentGroup = config.find_student_group(studentGroupId)
        if studentGroup:
            studentGroup.teachers.append(teacher.id)

    for assignmentGroupId in teacher.assignment_groups:
        assignmentGroup = config.find_assignment_group(assignmentGroupId)
        if assignmentGroup:
            assignmentGroup.teachers.append(teacher.id)

# Initialize a new Canvas object
canvas = Canvas(API_URL, course_config_start.api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course = canvas.get_course(course_config_start.course_id)

course = Course(canvas_course.id, canvas_course.name, actual_date.strftime(DATE_TIME_STR))
users = canvas_course.get_users(enrollment_type=['student'])

g_student_count = 0
g_students = {}
for user in users:
    g_student_count += 1
    student = Student(user.id, 0, user.name, 'None')
    g_students[user.id] = student

# ophalen secties en roles
course_sections = canvas_course.get_sections(include=['students'])
for course_section in course_sections:
    print("course_section", course_section)
    course_section_students = course_section.students
    if course_section_students:
        for section_student in course_section_students:
            role = config.find_role_by_section(course_section.id)
            if role:
                student_id = section_student["id"]
                if g_students.get(student_id):
                    g_students[student_id].roles.append(role)

for student in g_students.values():
    print(student)
    for perspective in config.perspectives:
        print(perspective.assignment_groups)
        if len(perspective.assignment_groups) > 1:
            new_perspective = Perspective(perspective.name)
            assignment_group_id = config.find_assignment_group_by_role(student.get_role())
            print("==>", student.get_role(), assignment_group_id)
            new_perspective.assignment_groups.append(assignment_group_id)
            student.perspectives.append(new_perspective)
        else:
            student.perspectives.append(perspective)


canvas_group_categories = canvas_course.get_group_categories()
for canvas_group_category in canvas_group_categories:
    print(canvas_group_category)
    if canvas_group_category.name == course_config_start.projects_groep_name:
        canvas_groups = canvas_group_category.get_groups()
        for canvas_group in canvas_groups:
            print(canvas_group)
            studentGroup = config.find_student_group(canvas_group.id)
            if studentGroup:
                canvas_users = canvas_group.get_users()
                for canvas_user in canvas_users:
                    if g_students.get(canvas_user.id):
                        student = g_students[canvas_user.id]
                        student.group_id = studentGroup.id
                        if len(studentGroup.teachers) > 0:
                            student.coach_initials = config.find_teacher(studentGroup.teachers[0]).initials
                        studentGroup.students.append(student)


with open(course_config_start.course_file_name, 'w') as f:
    dict_result = config.to_json(["assignment"])
    json.dump(dict_result, f, indent=2)

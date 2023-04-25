import json
from canvasapi import Canvas
from lib.config import API_URL, actual_date, group_id_dict
from lib.file import read_course_config_start, read_course_config
from model.Course import Course
from model.Perspective import Perspective
from model.Student import Student

course_config_start = read_course_config_start()
course_config = read_course_config(course_config_start.config_file_name)
print(course_config)

for teacher in course_config.teachers:
    for studentGroupId in teacher.projects:
        studentGroup = course_config.find_student_group(studentGroupId)
        if studentGroup:
            studentGroup.teachers.append(teacher.id)

    for assignmentGroupId in teacher.assignment_groups:
        assignmentGroup = course_config.find_assignment_group(assignmentGroupId)
        if assignmentGroup:
            assignmentGroup.teachers.append(teacher.id)

# Initialize a new Canvas object
canvas = Canvas(API_URL, course_config_start.api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course = canvas.get_course(course_config_start.course_id)
course = Course(canvas_course.id, canvas_course.name, actual_date.strftime("%A %d-%m-%Y"))
users = canvas_course.get_users(enrollment_type=['student'])
student_count = 0
for user in users:
    student_count += 1
    student = Student(user.id, 0, user.name, 'None')
    course.students[user.id] = student

# ophalen secties en roles
course_sections = canvas_course.get_sections(include=['students'])
for course_section in course_sections:
    print("course_section", course_section)
    course_section_students = course_section.students
    if course_section_students:
        for section_student in course_section_students:
            role = course_config.find_role_by_section(course_section.id)
            if role:
                student_id = section_student["id"]
                if course.students.get(student_id):
                    course.students[student_id].roles.append(role)

for student in course.students.values():
    for perspective in course_config.perspectives:
        if len(perspective.assignment_groups) > 1:
            new_perspective = Perspective(perspective.name)
            assignment_group_id = group_id_dict[student.roles[0]]
            new_perspective.assignment_groups.append(assignment_group_id)
            student.perspectives[perspective.name] = new_perspective
        else:
            student.perspectives[perspective.name] = perspective

canvas_group_categories = canvas_course.get_group_categories()
for canvas_group_category in canvas_group_categories:
    print(canvas_group_category)
    if canvas_group_category.name == course_config_start.projects_groep_name:
        canvas_groups = canvas_group_category.get_groups()
        for canvas_group in canvas_groups:
            print(canvas_group)
            studentGroup = course_config.find_student_group(canvas_group.id)
            canvas_users = canvas_group.get_users()
            for canvas_user in canvas_users:
                if course.students.get(canvas_user.id):
                    student = course.students[canvas_user.id]
                    student.group_id = studentGroup.id
                    if len(studentGroup.teachers) > 0:
                        student.coach_initials = course_config.find_teacher(studentGroup.teachers[0]).initials
                    studentGroup.students.append(student)

with open(course_config_start.course_file_name, 'w') as f:
    dict_result = course_config.to_json(["assignment"])
    json.dump(dict_result, f, indent=2)

# Haalt de studenten en de projecten op. Maakt een JSON waarin de url's naar de daily wordt opgeslagen.
from canvasapi import Canvas
import json
from datetime import timezone, datetime

from lib.file import read_course_config, read_course_config_start
from model.AssignmentDate import AssignmentDate
from model.Comment import Comment
from model.Course import *
from lib.config import actual_date, roles, API_URL

course_config_start = read_course_config_start()
course_config = read_course_config(course_config_start.config_file_name)

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
            if roles.get(course_section.name):
                student_id = section_student["id"]
                if course.students.get(student_id):
                    course.students[student_id].roles.append(roles[course_section.name])

with open("students.json", 'w') as f:
    dict_result = course.to_json([])
    json.dump(dict_result, f, indent=2)

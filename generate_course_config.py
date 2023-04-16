from canvasapi import Canvas
import json
from datetime import datetime

from lib.config import API_URL
from lib.file import read_course_config_start
from model.AssignmentGroup import AssignmentGroup
from model.Course import Course
from model.CourseConfig import CourseConfig
from model.Role import Role
from model.Section import Section
from model.StudentGroup import StudentGroup
from model.Teacher import Teacher

course_config_start = read_course_config_start()
# Initialize a new Canvas object
canvas = Canvas(API_URL, course_config_start.api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course = canvas.get_course(course_config_start.course_id)
actual_date = datetime.now()
course = Course(canvas_course.id, canvas_course.name, actual_date.strftime("%A %d-%m-%Y"))
course_config = CourseConfig(course_config_start.course_id, course.name, course_config_start.api_key)

#ophalen secties
course_sections = canvas_course.get_sections()
for course_section in course_sections:
    new_section = Section(course_section.id, course_section.name)
    course_config.sections.append(new_section)
    print("course_section", new_section)


# ophalen projectgroepen
canvas_group_categories = canvas_course.get_group_categories()
for canvas_group_category in canvas_group_categories:
    print(canvas_group_category)
    if canvas_group_category.name == "Project Groups":
        canvas_groups = canvas_group_category.get_groups()
        for canvas_group in canvas_groups:
            studentGroup = StudentGroup(canvas_group.id, canvas_group.name, 'Leeg')
            course_config.studentGroups.append(studentGroup)
            print(canvas_group)

# ophalen assignments_groups
canvas_assignment_groups = canvas_course.get_assignment_groups()
for canvas_assignment_group in canvas_assignment_groups:
    print("assignment_group", canvas_assignment_group)
    assignment_group = AssignmentGroup(canvas_assignment_group.id, canvas_assignment_group.name, "scale", 0, 0, 0)
    course_config.assignmentGroups.append(assignment_group)
    role = Role(canvas_assignment_group.name, canvas_assignment_group.name, canvas_assignment_group.id, 'btn-')
    course_config.roles.append(role)

# ophalen Teachers
users = canvas_course.get_users(enrollment_type=['teacher', 'ta'])
teacher_count = 0
for user in users:
    teacher_count += 1
    teacher = Teacher(user.id, user.name)
    course_config.teachers.append(teacher)
    print(teacher)

with open(course_config_start.config_file_name, 'w') as f:
    dict_result = course_config.to_json([])
    json.dump(dict_result, f, indent=2)

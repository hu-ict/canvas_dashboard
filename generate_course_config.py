from canvasapi import Canvas
import json
from datetime import datetime

from lib.config import API_URL, end_date, getDateTimeStr
from lib.file import read_course_config_start
from model.Assignment import Assignment
from model.AssignmentDate import AssignmentDate
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
course_config = CourseConfig(course.name)

#ophalen secties
course_sections = canvas_course.get_sections()
for course_section in course_sections:
    new_section = Section(course_section.id, course_section.name, "role")
    course_config.sections.append(new_section)
    print("course_section", new_section)

# ophalen assignments_groups and score
canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides'])
for canvas_assignment_group in canvas_assignment_groups:
    print("assignment_group", canvas_assignment_group)
    group_points_possible = 0
    assignment_group = AssignmentGroup(canvas_assignment_group.id, canvas_assignment_group.name, [], "scale", 0, 0, 0)
    for canvas_assignment in canvas_assignment_group.assignments:
        if canvas_assignment['overrides']:
            for overrides in canvas_assignment['overrides']:
                if canvas_assignment['points_possible']:
                    group_points_possible += canvas_assignment['points_possible']
                    points_possible = canvas_assignment['points_possible']
                else:
                    points_possible = 0

                if overrides['lock_at']:
                    assignment_date = overrides['lock_at']
                else:
                    if overrides['due_at']:
                        assignment_date = overrides['due_at']
                    else:
                        assignment_date = getDateTimeStr(end_date)
                if 'course_section_id' in overrides.keys():
                    section_id = overrides['course_section_id']
                else:
                    section_id = 0
                assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'], canvas_assignment['assignment_group_id'], section_id, points_possible, assignment_date)
                assignment_group.assignments.append(assignment)
        else:
            if canvas_assignment['points_possible']:
                group_points_possible += canvas_assignment['points_possible']
                points_possible = canvas_assignment['points_possible']
            else:
                points_possible = 0

            if canvas_assignment['lock_at']:
                assignment_date = canvas_assignment['lock_at']
            else:
                if canvas_assignment['due_at']:
                    assignment_date = canvas_assignment['due_at']
                else:
                    assignment_date = getDateTimeStr(end_date)
            assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'],
                                    canvas_assignment['assignment_group_id'], 0,
                                    points_possible, assignment_date)
            assignment_group.assignments.append(assignment)

    assignment_group.total_points = group_points_possible
    print("assignment_group", canvas_assignment_group, group_points_possible)
    course_config.assignmentGroups.append(assignment_group)

# ophalen Teachers
users = canvas_course.get_users(enrollment_type=['teacher', 'ta'])
teacher_count = 0
for user in users:
    teacher_count += 1
    teacher = Teacher(user.id, user.name)
    course_config.teachers.append(teacher)
    print(teacher)

# ophalen projectgroepen
canvas_group_categories = canvas_course.get_group_categories()
for canvas_group_category in canvas_group_categories:
    print(canvas_group_category)
    if canvas_group_category.name == course_config_start.projects_groep_name:
        canvas_groups = canvas_group_category.get_groups()
        for canvas_group in canvas_groups:
            studentGroup = StudentGroup(canvas_group.id, canvas_group.name, 'teacher')
            course_config.studentGroups.append(studentGroup)
            print(canvas_group)

course_config.perspectives = course_config_start.perspectives

print(course_config_start)

with open(course_config_start.config_file_name, 'w') as f:
    dict_result = course_config.to_json(["assignment"])
    json.dump(dict_result, f, indent=2)

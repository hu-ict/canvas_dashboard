import json
from canvasapi import Canvas
from lib.config import API_URL, actual_date, DATE_TIME_STR, get_date_time_obj
from lib.file import read_start, read_config
from model.Assignment import Assignment
from model.Perspective import Perspective
from model.Student import Student

def get_dates(input):
    if input['lock_at']:
        assignment_date = get_date_time_obj(input['lock_at'])
    else:
        if input['due_at']:
            assignment_date = get_date_time_obj(input['due_at'])
        else:
            assignment_date = course_config_start.end_date
    if input['unlock_at']:
        unlock_date = get_date_time_obj(input['unlock_at'])
    else:
        unlock_date = course_config_start.start_date
    return unlock_date, assignment_date


def link_teachers():
    print('Link teachers to student_groups and assignment_groups')
    for teacher in config.teachers:
        for studentGroupId in teacher.projects:
            studentGroup = config.find_student_group(studentGroupId)
            if studentGroup:
                studentGroup.teachers.append(teacher.id)
        for assignmentGroupId in teacher.assignment_groups:
            assignmentGroup = config.find_assignment_group(assignmentGroupId)
            if assignmentGroup:
                assignmentGroup.teachers.append(teacher.id)

course_config_start = read_start()
config = read_config(course_config_start.config_file_name)
print(config)


# Initialize a new Canvas object
canvas = Canvas(API_URL, course_config_start.api_key)
user = canvas.get_current_user()
print(user.name)

canvas_course = canvas.get_course(course_config_start.course_id)

link_teachers()

# course = Course(canvas_course.id, canvas_course.name, actual_date.strftime(DATE_TIME_STR))

# Ophalen Students
users = canvas_course.get_users(enrollment_type=['student'])
config.students = []
for user in users:
    student = Student(user.id, 0, user.name, 'None')
    config.students.append(student)

# Ophalen canvas_pages
pages = canvas_course.get_pages()
for page in pages:
    print(f"{page.published:1};{page.title};{page.url}")


# Ophalen Secties en Roles
course_sections = canvas_course.get_sections(include=['students'])
for course_section in course_sections:
    # use only relevant sections
    section = config.find_section(course_section.id)
    if section:
        print("course_section", section)
        course_section_students = course_section.students
        if course_section_students:
            for section_student in course_section_students:
                student_id = section_student["id"]
                student = config.find_student(student_id)
                if student:
                    student.roles.append(section.role)

for student in config.students:
    if len(student.roles) == 0:
        config.students.remove(student)
config.student_count = len(config.students)

# Perspectives toevoegen aan Students
for student in config.students:
    for perspective in config.perspectives:
        # print(perspective.assignment_groups)
        if len(perspective.assignment_groups) > 1:
            new_perspective = Perspective(perspective.name)
            assignment_group_id = config.find_assignment_group_by_role(student.get_role())
            new_perspective.assignment_groups.append(assignment_group_id)
            student.perspectives.append(new_perspective)
        else:
            student.perspectives.append(perspective)

# Students en StudentGroups koppelen
canvas_group_categories = canvas_course.get_group_categories()
for canvas_group_category in canvas_group_categories:
    print(canvas_group_category)
    # ophalen projectgroepen
    if canvas_group_category.name == course_config_start.projects_groep_name:
        canvas_groups = canvas_group_category.get_groups()
        for canvas_group in canvas_groups:
            print(canvas_group)
            studentGroup = config.find_student_group(canvas_group.id)
            if studentGroup:
                canvas_users = canvas_group.get_users()
                for canvas_user in canvas_users:
                    student = config.find_student(canvas_user.id)
                    if student:
                        student.group_id = studentGroup.id
                        if len(studentGroup.teachers) > 0:
                            student.coach_initials = config.find_teacher(studentGroup.teachers[0]).initials
                        studentGroup.students.append(student)
    # ophalen slb-groepen
    if canvas_group_category.name == course_config_start.slb_groep_name:
        canvas_groups = canvas_group_category.get_groups()
        for canvas_group in canvas_groups:
            print(canvas_group)
            slb_group = config.find_slb_group(canvas_group.id)
            if slb_group:
                canvas_users = canvas_group.get_users()
                for canvas_user in canvas_users:
                    student = config.find_student(canvas_user.id)
                    if student:
                        slb_group.students.append(student)

# Ophalen Assignments bij de AssignmentsGroups
canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides'])
for canvas_assignment_group in canvas_assignment_groups:
    # use only relevant assignment_groups
    assignment_group = config.find_assignment_group(canvas_assignment_group.id)
    if assignment_group:
        print("assignment_group", canvas_assignment_group)
        group_points_possible = 0
        for canvas_assignment in canvas_assignment_group.assignments:
            if canvas_assignment['points_possible']:
                group_points_possible += canvas_assignment['points_possible']
                points_possible = canvas_assignment['points_possible']
            else:
                points_possible = 0


            if canvas_assignment['overrides']:
                for overrides in canvas_assignment['overrides']:
                    unlock_date, assignment_date = get_dates(overrides)
                    if 'course_section_id' in overrides.keys():
                        section_id = overrides['course_section_id']
                    else:
                        section_id = 0
                    assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'], canvas_assignment['assignment_group_id'], section_id, points_possible, assignment_date, unlock_date)
                    print("OVERRIDE", assignment)
                    assignment_group.append_assignment(assignment)
            else:
                unlock_date, assignment_date = get_dates(canvas_assignment)
                section_id = 0
                assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'],
                                    canvas_assignment['assignment_group_id'], section_id,
                                    points_possible, assignment_date, unlock_date)
                print(assignment)
                assignment_group.append_assignment(assignment)
        print(assignment_group.name, assignment_group.total_points, group_points_possible)
        # assignment_group.total_points = group_points_possible

with open(course_config_start.course_file_name, 'w') as f:
    dict_result = config.to_json(["assignment"])
    json.dump(dict_result, f, indent=2)

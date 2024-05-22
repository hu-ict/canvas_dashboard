import json
import sys

from canvasapi import Canvas
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import API_URL, get_date_time_obj, date_to_day, get_actual_date
from lib.file import read_start, read_config, read_course_instance
from model.Student import Student
from model.perspective.StudentPerspective import StudentPerspective
from model.perspective.StudentProgress import StudentProgress


def link_teachers(config):
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


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("C01 -", "Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_config(start.course_file_name)
    print("C02 -", "Config", course)
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("C03 -", user.name)
    canvas_course = canvas.get_course(start.canvas_course_id)
    link_teachers(course)
    # Ophalen Students
    print("C04 -", "Ophalen studenten")
    users = canvas_course.get_users(enrollment_type=['student'])
    course.students = []
    student_count = 0
    for user in users:
        if hasattr(user, 'login_id'):
            print("C11 -", user.name, user.login_id)
            student = Student(user.id, 0, user.name, user.sortable_name, 'None', "", user.login_id, "", 0)
            course.students.append(student)
            student_count += 1
            # if student_count > 100:
            #     break
    # Ophalen Secties en Roles
    print("C05 -", "Ophalen student secties uit Canvas deze koppelen aan Role ")
    canvas_sections = canvas_course.get_sections(include=['students'])
    for course_section in canvas_sections:
        # use only relevant sections
        section = course.find_section(course_section.id)
        if section:
            course_section_students = course_section.students
            if course_section_students:
                for section_student in course_section_students:
                    student_id = section_student["id"]
                    student = course.find_student(student_id)
                    if student:
                        student.role = section.role
                    else:
                        print("C21 -", "Student not found", section_student["id"])
            else:
                print("C22 -", "No students in section", course_section.name)
        else:
            print("C23 -", "Section not found", course_section.name)

    print("C07 -", "Opschonen studenten zonder Role")
    for student in course.students:
        if len(student.role) == 0:
            course.students.remove(student)
    course.student_count = len(course.students)

    # StudentProgress toevoegen aan Students
    for student in course.students:
        student.student_progress = StudentProgress(course.progress.name, course.progress.assignment_groups)
    # Perspectives toevoegen aan Students
    for student in course.students:
        student.perspectives = {}
        for perspective in course.perspectives.values():
            if len(perspective.assignment_groups) > 1:
                # meerdere assignment_group: kennis
                student.perspectives[perspective.name] = StudentPerspective(perspective.name, 0, 0, 0)
                assignment_group_id = course.find_assignment_group_by_role(student.role)
                student.perspectives[perspective.name].assignment_groups.append(assignment_group_id)
            elif len(perspective.assignment_groups) == 1:
                # één assignment_group: team, gilde en peil
                student.perspectives[perspective.name] = StudentPerspective(perspective.name, 0, 0, 0)
                assignment_group_id = course.perspectives[perspective.name].assignment_groups[0]
                student.perspectives[perspective.name].assignment_groups.append(assignment_group_id)
            else:
                print("C31 - ERROR: geen assignment_group for perspective")


    # Students en StudentGroups koppelen
    canvas_group_categories = canvas_course.get_group_categories()

    for canvas_group_category in canvas_group_categories:
        print("C41 -", canvas_group_category)
        # ophalen projectgroepen
        if canvas_group_category.name == start.projects_groep_name:
            canvas_groups = canvas_group_category.get_groups()
            for canvas_group in canvas_groups:
                print("C42 -", canvas_group)
                studentGroup = course.find_student_group(canvas_group.id)
                if studentGroup:
                    canvas_users = canvas_group.get_users()
                    for canvas_user in canvas_users:
                        student = course.find_student(canvas_user.id)
                        if student:
                            student.group_id = studentGroup.id
                            if len(studentGroup.teachers) > 0:
                                student.coach = studentGroup.teachers[0]
                            studentGroup.students.append(student)
                        else:
                            print("C43 - Student in Canvas project group not found", canvas_user.id)
        # ophalen slb-groepen
        if start.slb_groep_name is not None and canvas_group_category.name == start.slb_groep_name:
            canvas_groups = canvas_group_category.get_groups()
            for canvas_group in canvas_groups:
                print("C45 -", canvas_group)
                slb_group = course.find_slb_group(canvas_group.id)
                if slb_group:
                    canvas_users = canvas_group.get_users()
                    for canvas_user in canvas_users:
                        student = course.find_student(canvas_user.id)
                        if student:
                            slb_group.students.append(student)
                        else:
                            print("C46 - Student in Canvas slb group not found", canvas_user.id)

        for role in course.roles:
            students = course.find_students_by_role(role.short)
            role.students = students


    for student_group in course.student_groups:
        student_group.students = sorted(student_group.students, key=lambda s: s.sortable_name)

    for role in course.roles:
        role.students = sorted(role.students, key=lambda s: s.sortable_name)


    with open(start.course_file_name, 'w') as f:
        dict_result = course.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)


if __name__ == "__main__":
    print("generate_students.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
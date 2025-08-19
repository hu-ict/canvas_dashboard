import json
import sys

from canvasapi import Canvas
from lib.lib_date import API_URL, get_actual_date
from lib.file import read_start, read_course_instances, read_course
from model.Student import Student
from model.StudentGroup import StudentGroup
from model.StudentLink import StudentLink


def get_groups(start, course, canvas_course):
    group_list = []
    if start.project_group_name == "SECTIONS":
        print("GST21 - Werken met Canvas secties als groepen (meestal S1 propedeuse).")
        for section in course.sections:
            student_group = StudentGroup(section.id, section.name)
            course.project_groups.append(student_group)
    else:
        canvas_group_categories = canvas_course.get_group_categories()
        for canvas_group_category in canvas_group_categories:
            # print("GCONF20 -", canvas_group_category, start1.project_group_name, start1.guild_group_name)
            # retrieve project_groups
            if canvas_group_category.name == start.project_group_name:
                canvas_groups = canvas_group_category.get_groups()
                for canvas_group in canvas_groups:
                    student_group = StudentGroup(canvas_group.id, canvas_group.name)
                    course.project_groups.append(student_group)
                    print("GST23 - project_group", canvas_group)
            elif canvas_group_category.name == start.guild_group_name:
                canvas_groups = canvas_group_category.get_groups()
                for canvas_group in canvas_groups:
                    student_group = StudentGroup(canvas_group.id, canvas_group.name)
                    course.guild_groups.append(student_group)
                    print("GST24 - guild_group", canvas_group)
            else:
                print("GST25 - onbekende group_category", canvas_group_category.name)


def get_students_in_groups(start, course, canvas_course):
    if start.project_group_name == "SECTIONS":
        print("GST31 - Werken met Canvas secties als groepen (meestal S1 propedeuse).")
    else:
        canvas_group_categories = canvas_course.get_group_categories()
        for canvas_group_category in canvas_group_categories:
            print("GST32 -", canvas_group_category)
            # Link students to project_groups
            if canvas_group_category.name == start.project_group_name:
                print("GST33 - Link students to project_groups", canvas_group_category.name)
                link_students_to_project_groups(course, canvas_group_category.get_groups())
            if canvas_group_category.name == start.guild_group_name:
                print("GST34 - Link students to guild_groups", canvas_group_category.name)
                link_students_to_guild_groups(course, canvas_group_category.get_groups())


def link_teachers_to_project_group(course):
    print('GS41 - Link teachers to project_groups and students')
    for teacher in course.teachers:
        for student_group_id in teacher.project_groups:
            # zoeken naar project_group en nummer of naam
            student_group = course.find_project_group(student_group_id)
            if student_group is None:
                # zoeken op naam
                student_group = course.find_project_group_by_name(student_group_id)
                if student_group is not None:
                    student_group.teachers.append(teacher.id)
                print("GST43 - student_group", student_group_id, student_group)
            else:
                student_group.teachers.append(teacher.id)
                print("GST44 - student_group", student_group_id, student_group)
            if student_group is not None:
                for student_link in student_group.students:
                    student = course.find_student(student_link.id)
                    student.project_teachers.append(teacher.id)
            else:
                print("GST45 - geen student_group voor", student_group_id)


def link_teachers_to_guild_group(course):
    print('GS51 - Link teachers to guild_groups')
    for teacher in course.teachers:
        for student_group_id in teacher.guild_groups:
            # zoeken naar guild_group en nummer of naam
            student_group = course.find_guild_group(student_group_id)
            if student_group is None:
                # zoeken op naam
                student_group = course.find_guild_group_by_name(student_group_id)
                if student_group is not None:
                    student_group.teachers.append(teacher.id)
                print("GST53 - student_group", student_group_id, student_group)
            else:
                student_group.teachers.append(teacher.id)
                print("GST54 - student_group", student_group_id, student_group)
            for student_link in student_group.students:
                student = course.find_student(student_link.id)
                student.guild_teachers.append(teacher.id)


def get_section_students(start, course, canvas_course):
    # Ophalen Secties en Roles
    print("GST61 -", "Ophalen students and secties uit Canvas deze koppelen aan Role ")
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
                    if student is not None:
                        if start.project_group_name == "SECTIONS":
                            project_group = course.find_project_group_by_name(section.name)
                            # print("GST63 -", section.name, project_group)
                            if project_group:
                                student.project_id = project_group.id
                                for teacher_id in project_group.teachers:
                                    student.project_teachers.append(teacher_id)
                                student_link = StudentLink.from_student(student)
                                # print("GS64 -", student_link)
                                project_group.students.append(student_link)
                            else:
                                print(f"GST65 - ERROR - section.name ({section.name}) not found in list student_group for student {student.name}.")
                        student.role = section.role
                        if student.role is None:
                            print("GST66 - student.role is leeg", student.name)
                    else:
                        print("GST67 -", "Student not found", section_student["id"], "from section", section)
            else:
                print("GST68 -", "No students in section", course_section.name)
        else:
            print("GST69 -", "Section not found", course_section.name)


def link_students_to_role(course):
    # Link students to roles
    print("GS71 - Link students to roles")
    for role in course.roles:
        students = course.find_students_by_role(role.short)
        for student in students:
            student_link = StudentLink.from_student(student)
            # print("GS73 -", student_link)
            role.students.append(student_link)


def link_students_to_project_groups(course, canvas_groups):
    # dit zijn de project_groups of de guild_groups
    print("GST81 - link_students_to_project_groups")
    for canvas_group in canvas_groups:
        print("GST82 -", canvas_group)
        student_group = course.find_project_group(canvas_group.id)
        if student_group:
            canvas_users = canvas_group.get_users()
            for canvas_user in canvas_users:
                student = course.find_student(canvas_user.id)
                # print("GST84 - Student", student)
                if student:
                    # print("GST85 - Student", student)
                    student.project_id = student_group.id
                    for teacher_id in student_group.teachers:
                        student.project_teachers.append(teacher_id)
                    student_link = StudentLink.from_student(student)
                    # print("GS86 -", student_link)
                    student_group.students.append(student_link)
                else:
                    print("GST87 - Student in Canvas project_group not found", canvas_user.id, canvas_user.name)


def link_students_to_guild_groups(course, canvas_groups):
    # dit zijn de project_groups of de guild_groups
    print("GST91 - link_students_to_guild_groups")
    for canvas_group in canvas_groups:
        print("GST92 -", canvas_group)
        student_group = course.find_guild_group(canvas_group.id)
        if student_group:
            print("GTS93 -", student_group)
            canvas_users = canvas_group.get_users()
            for canvas_user in canvas_users:
                student = course.find_student(canvas_user.id)
                if student:
                    print("GTS94 -", student.name)
                    student.guild_id = student_group.id
                    for teacher_id in student_group.teachers:
                        student.guild_teachers.append(teacher_id)
                    student_link = StudentLink.from_student(student)
                    # print("GS95 -", student_link)
                    student_group.students.append(student_link)
                else:
                    print("GST96 - Student in Canvas guild group not found", canvas_user.id, canvas_user.name)


def generate_students(instance_name):
    print("GS001 - generate_students.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("GST002 - Instance:", instance.name)
    start = read_start(instance.get_start_file_name())
    course = read_course(instance.get_course_file_name())
    # print("GS02 -", "Config", course)
    # Initialize a new Canvas object
    print(API_URL, start.api_key)
    canvas = Canvas(API_URL, start.api_key)
    current_user = canvas.get_current_user()
    print("GST003 -", current_user.name)
    # cleanup students in list roles and project_groups
    for role in course.roles:
        role.students = []
    canvas_course = canvas.get_course(course.canvas_id)
    # Ophalen Students
    print("GS005 - Retrieve students")
    course.students = []
    canvas_users = canvas_course.get_users(enrollment_type=['student'], include=["enrollments"])
    for canvas_user in canvas_users:
        if hasattr(canvas_user, 'login_id'):
            print("GST007 - Create student", canvas_user.name, canvas_user.login_id, canvas_user.sis_user_id)
            student = Student(canvas_user.id, 0, 0, canvas_user.name, canvas_user.sis_user_id, canvas_user.sortable_name, "", canvas_user.login_id, "")
            course.students.append(student)
        else:
            if hasattr(canvas_user, 'sis_user_id'):
                print("GST008 - Create student without login_id", canvas_user.name, canvas_user.sis_user_id)
                student = Student(canvas_user.id, 0, 0, canvas_user.name, canvas_user.sis_user_id, canvas_user.sortable_name, "", "", "")
                # print("GS17 ", student)
                course.students.append(student)
    print("GST009 - Aantal studenten", len(course.students))
    for student in course.students:
        print("GST010 -", student)
    course.project_groups = []
    course.guild_groups = []
    get_groups(start, course, canvas_course)
    get_section_students(start, course, canvas_course)
    get_students_in_groups(start, course, canvas_course)
    link_students_to_role(course)
    link_teachers_to_project_group(course)
    if len(start.guild_group_name) > 0:
        link_teachers_to_guild_group(course)

    print("GST011 - Opschonen studenten zonder Role, totaal", len(course.students))
    without_role = 0
    course_students = course.students.copy()
    for student in course_students:
        # print("GST23 -", student.name, "["+student.role+"]")
        if len(student.role) == 0:
            print("GST012 - Verwijder student uit lijst, heeft geen role", student.name)
            course.remove_student(student.id)
            without_role += 1
    print("GST013 - Opschonen studenten zonder ProjectGroup")
    course_students = course.students.copy()
    without_project = 0
    for student in course_students:
        # print("GST014 -", student.name, "["+student.role+"]")
        if student.project_id == 0:
            print("GST015 - Verwijder student uit lijst, heeft geen project", student.name)
            course.remove_student(student.id)
            without_project += 1

    course.student_count = len(course.students)

    for student_group in course.project_groups:
        student_group.students = sorted(student_group.students, key=lambda s: s.sortable_name)
    for student_group in course.guild_groups:
        student_group.students = sorted(student_group.students, key=lambda s: s.sortable_name)
    for role in course.roles:
        role.students = sorted(role.students, key=lambda s: s.sortable_name)

    print("GST016 - Aantal Canvas studenten", len(course.students))
    for student in course.students:
        print("GST017 -", student)

    with open(instance.get_course_file_name(), 'w') as f:
        dict_result = course.to_json()
        json.dump(dict_result, f, indent=2)

    print("GST99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_students(sys.argv[1])
    else:
        generate_students("")

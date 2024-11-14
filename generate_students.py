import json
import sys

from canvasapi import Canvas
from lib.lib_date import API_URL, get_actual_date
from lib.file import read_start, read_course_instances, read_course
from model.Student import Student
from model.StudentLink import StudentLink


def link_teachers(config):
    print('GS21 - Link teachers to student_groups')
    for teacher in config.teachers:
        for studentGroupId in teacher.teams:
            studentGroup = config.find_student_group(studentGroupId)
            if studentGroup is not None:
                studentGroup.teachers.append(teacher.id)
            else:
                # print("GS22 - studentGroupName", studentGroupId)
                studentGroup = config.find_student_group_by_name(studentGroupId)
                if studentGroup is not None:
                    studentGroup.teachers.append(teacher.id)


def get_section_students(canvas_course, start, course):
    # Ophalen Secties en Roles
    print("GS21 -", "Ophalen students and secties uit Canvas deze koppelen aan Role ")
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
                        if start.projects_groep_name == "SECTIONS":
                            student_group = course.find_student_group_by_name(section.name)
                            # print("GS24 -", section.name)
                            if student_group:
                                student.group_id = student_group.id
                                if len(student_group.teachers) > 0:
                                    student.coach = student_group.teachers[0]
                                student_link = StudentLink.from_student(student)
                                # print("GS41 -", student_link)
                                student_group.students.append(student_link)
                            else:
                                print(f"GS25 - ERROR - section.name ({section.name}) not found in list student_group for student {student.name}.")
                        student.role = section.role
                        if student.role is None:
                            print("GS26 - Student.Role", student.name)
                    else:
                        print("GS27 -", "Student not found", section_student["id"])
            else:
                print("GS28 -", "No students in section", course_section.name)
        else:
            print("GS29 -", "Section not found", course_section.name)

def link_students_to_role(course):
    # Link students to roles
    print("GS50 - Link students to roles")
    for role in course.roles:
        students = course.find_students_by_role(role.short)
        for student in students:
            student_link = StudentLink.from_student(student)
            # print("GS53 -", student_link)
            role.students.append(student_link)


def generate_students(instance_name):
    print("GS01 - generate_students.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("GST02 - Instance:", instance.name)
    start = read_start(instance.get_start_file_name())
    course = read_course(instance.get_course_file_name())
    # print("GS02 -", "Config", course)
    # Initialize a new Canvas object
    print(API_URL, start.api_key)
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GST03 -", user.name)
    # cleanup students in list roles and project_groups
    for role in course.roles:
        role.students = []
    for student_group in course.student_groups:
        student_group.students = []
        student_group.teachers = []
    canvas_course = canvas.get_course(course.canvas_id)
    # Ophalen Students
    print("GS13 - Retrieve students")
    course.students = []
    users = canvas_course.get_users(enrollment_type=['student'], include=["enrollments"])
    student_count = 0
    for user in users:
        if hasattr(user, 'login_id'):
            print("GST15 - Create student", user.name, user.login_id, user.sis_user_id)
            student = Student(user.id, 0, user.name, user.sis_user_id, user.sortable_name, 0, "", user.login_id, "")
        else:
            print("GST16 - Create student without login_id", user.name, user.sis_user_id)
            student = Student(user.id, 0, user.name, user.sis_user_id, user.sortable_name, 0, "", "", "")
        # print("GS17 ", student)
        course.students.append(student)
        student_count += 1
    print("GST18 - Aantal Canvas users", student_count)

    get_section_students(canvas_course, start, course)

    link_teachers(course)


    print("GST07 - Opschonen studenten zonder Role")
    for student in course.students:
        if len(student.role) == 0:
            print("GST95 - Verwijder student uit lijst, heeft geen role", student.name)
            course.students.remove(student)
    if start.projects_groep_name == "SECTIONS":
        print("GST36 - Werken met Canvas secties als groepen.")
    else:
        canvas_group_categories = canvas_course.get_group_categories()
        for canvas_group_category in canvas_group_categories:
            print("GST37 -", canvas_group_category)
            # Link students to student_groups
            if canvas_group_category.name == start.projects_groep_name:
                print("GST38 - Link students to student_groups")
                canvas_groups = canvas_group_category.get_groups()
                for canvas_group in canvas_groups:
                    print("GST40 -", canvas_group)
                    student_group = course.find_student_group(canvas_group.id)
                    if student_group:
                        canvas_users = canvas_group.get_users()
                        for canvas_user in canvas_users:
                            student = course.find_student(canvas_user.id)
                            if student:
                                student.group_id = student_group.id
                                if len(student_group.teachers) > 0:
                                    student.coach = student_group.teachers[0]
                                student_link = StudentLink.from_student(student)
                                # print("GS41 -", student_link)
                                student_group.students.append(student_link)
                            else:
                                print("GST42 - Student in Canvas project group not found", canvas_user.id, canvas_user.name)

    link_students_to_role(course)

    for student_group in course.student_groups:
        student_group.students = sorted(student_group.students, key=lambda s: s.sortable_name)

    print("GST08 - Opschonen studenten zonder StudentGroup")
    for student in course.students:
        if not course.exists_in_team(student.id):
            print("GST95 - Verwijder student uit lijst, heeft geen team", student.name)
            course.students.remove(student)
    course.student_count = len(course.students)

    for role in course.roles:
        role.students = sorted(role.students, key=lambda s: s.sortable_name)

    with open(instance.get_course_file_name(), 'w') as f:
        dict_result = course.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)

    print("GST99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_students(sys.argv[1])
    else:
        generate_students("")

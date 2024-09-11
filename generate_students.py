import json
import sys

from canvasapi import Canvas
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import API_URL, get_date_time_obj, date_to_day, get_actual_date
from lib.file import read_start, read_config, read_course_instance, read_course
from model.Student import Student
from model.StudentLink import StudentLink
from model.perspective.AttendancePerspective import AttendancePerspective
from model.perspective.StudentPerspective import StudentPerspective
from model.perspective.StudentLevelMoments import StudentLevelMoments


def link_teachers(config):
    print('GS15 - Link teachers to student_groups')
    for teacher in config.teachers:
        for studentGroupId in teacher.teams:
            studentGroup = config.find_student_group(studentGroupId)
            if studentGroup is not None:
                studentGroup.teachers.append(teacher.id)
            else:
                print("GS16 - studentGroupName", studentGroupId)
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
                            print("GS24 -", section.name)
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
                    else:
                        print("GS27 -", "Student not found", section_student["id"])
            else:
                print("GS28 -", "No students in section", course_section.name)
        else:
            print("GS29 -", "Section not found", course_section.name)

def add_perspectives_to_students(start, course):
    # StudentProgress toevoegen aan Students
    if course.level_moments is not None:
        for student in course.students:
            student.student_level_moments = StudentLevelMoments(course.level_moments.name, course.level_moments.assignment_groups)
    if course.attendance is not None:
        for student in course.students:
            student.attendance = AttendancePerspective(course.attendance.name, -1, 0, 0)
    # Perspectives toevoegen aan Students
    for student in course.students:
        student.perspectives = {}
        for perspective in course.perspectives.values():
            if len(perspective.assignment_groups) > 1:
                # meerdere assignment_group: kennis
                student.perspectives[perspective.name] = StudentPerspective(perspective.name, -1, 0, 0)
                assignment_group_id = course.find_assignment_group_by_role(student.role)
                student.perspectives[perspective.name].assignment_groups.append(assignment_group_id)
            elif len(perspective.assignment_groups) == 1:
                # één assignment_group: team, gilde en peil
                student.perspectives[perspective.name] = StudentPerspective(perspective.name, -1, 0, 0)
                assignment_group_id = course.perspectives[perspective.name].assignment_groups[0]
                student.perspectives[perspective.name].assignment_groups.append(assignment_group_id)
            else:
                print("GS31 - ERROR: geen assignment_group for perspective")
        student.attendance_perspective = AttendancePerspective("attendance", -1, 0, 0)


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GS02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(instances.get_course_file_name(instances.current_instance))
    # print("GS02 -", "Config", course)
    # Initialize a new Canvas object
    print(API_URL, start.api_key)
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GS03 -", user.name)
    # cleanup students in list roles, slb and project_groups
    for role in course.roles:
        role.students = []
    for student_group in course.student_groups:
        student_group.students = []
        student_group.teachers = []
    for slb_group in course.slb_groups:
        slb_group.students = []


    canvas_course = canvas.get_course(start.canvas_course_id)
    # Ophalen Students
    print("GS13 - Retrieve students")
    course.students = []
    users = canvas_course.get_users(enrollment_type=['student'], include=["enrollments"])
    student_count = 0
    for user in users:
        if hasattr(user, 'login_id'):
            print("GS15 - Create student", user.name, user.login_id)
            student = Student(user.id, 0, user.name, user.sortable_name, 0, "", user.login_id, "", 0)
        else:
            print("GS16 - Create student without login_id", user.name)
            student = Student(user.id, 0, user.name, user.sortable_name, 0, "", "", "", 0)
        course.students.append(student)
        student_count += 1
    print("GS18 - Aantal Canvas users", student_count)

    get_section_students(canvas_course, start, course)

    link_teachers(course)


    print("GS07 - Opschonen studenten zonder Role")
    for student in course.students:
        if len(student.role) == 0:
            print("GS95 - Verwijder student uit lijst, heeft geen role", student.name)
            course.students.remove(student)

    add_perspectives_to_students(start, course)

    # Students en StudentGroups koppelen
    if start.slb_groep_name is None and start.projects_groep_name == "SECTIONS":
        print("GS36 - Werken met Canvas secties als groepen.")
    else:
        canvas_group_categories = canvas_course.get_group_categories()
        for canvas_group_category in canvas_group_categories:
            print("GS37 -", canvas_group_category)
            # Link students to student_groups
            if canvas_group_category.name == start.projects_groep_name:
                print("GS38 - Link students to student_groups")
                canvas_groups = canvas_group_category.get_groups()
                for canvas_group in canvas_groups:
                    print("GS40 -", canvas_group)
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
                                print("GS42 - Student in Canvas project group not found", canvas_user.id, canvas_user.name)
            # Link students to slb_groups
            if start.slb_groep_name is not None and canvas_group_category.name == start.slb_groep_name:
                print("GS45 - Link students to slb_groups")
                canvas_groups = canvas_group_category.get_groups()
                for canvas_group in canvas_groups:
                    print("GS47 - canvas_group", canvas_group)
                    slb_group = course.find_slb_group(canvas_group.id)
                    if slb_group:
                        canvas_users = canvas_group.get_users()
                        for canvas_user in canvas_users:
                            student = course.find_student(canvas_user.id)
                            if student:
                                student_link = StudentLink.from_student(student)
                                # print("GS48 -", student_link)
                                slb_group.students.append(student_link)
                            else:
                                print("GS49 - Student in Canvas slb group not found", canvas_user.id)
    # Link students to roles
    print("GS50 - Link students to roles")
    for role in course.roles:
        students = course.find_students_by_role(role.short)
        for student in students:
            student_link = StudentLink.from_student(student)
            # print("GS53 -", student_link)
            role.students.append(student_link)

    for student_group in course.student_groups:
        student_group.students = sorted(student_group.students, key=lambda s: s.sortable_name)

    print("GS08 - Opschonen studenten zonder StudentGroup")
    for student in course.students:
        if not course.exists_in_team(student.id):
            print("GS95 - Verwijder student uit lijst, heeft geen team", student.name)
            course.students.remove(student)
    course.student_count = len(course.students)

    for role in course.roles:
        role.students = sorted(role.students, key=lambda s: s.sortable_name)

    with open(instances.get_course_file_name(instances.current_instance), 'w') as f:
        dict_result = course.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)

    print("GS99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GS01 - generate_students.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
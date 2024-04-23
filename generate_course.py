import json
import sys

from canvasapi import Canvas
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import API_URL, get_date_time_obj, date_to_day, get_actual_date
from lib.file import read_start, read_config, read_course_instance
from model.Assignment import Assignment
from model.Criterion import Criterion
from model.Rating import Rating
from model.Student import Student
from model.perspective.StudentPerspective import StudentPerspective
from model.perspective.StudentProgress import StudentProgress


def get_dates(start, input):
    if input.due_at:
        assignment_date = get_date_time_obj(input.due_at)
    else:
        if input.lock_at:
            assignment_date = get_date_time_obj(input.lock_at)
        else:
            assignment_date = start.end_date
    if input.unlock_at:
        unlock_date = get_date_time_obj(input.unlock_at)
    else:
        unlock_date = start.start_date
    return unlock_date, assignment_date

def get_rubrics(canvas_rubrics):
    # print("C74 -", canvas_assignment)
    rubrics_points = 0
    rubrics = []
    for canvas_criterium in canvas_rubrics:
        criterion = Criterion(canvas_criterium['id'], canvas_criterium['points'], canvas_criterium['description'])
        rubrics_points += criterion.points
        rubrics.append(criterion)
        for canvas_rating in canvas_criterium['ratings']:
            criterion.ratings.append(Rating(canvas_rating['id'], canvas_rating['points'], canvas_rating['description']))
    return rubrics, rubrics_points


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
    config = read_config(start.config_file_name)
    print("C02 -", "Config", config)
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("C03 -", user.name)
    canvas_course = canvas.get_course(start.canvas_course_id)
    link_teachers(config)
    # Ophalen Students
    print("C04 -", "Ophalen studenten")
    users = canvas_course.get_users(enrollment_type=['student'])
    config.students = []
    student_count = 0
    for user in users:
        if hasattr(user, 'login_id'):
            print("C11 -", user.name, user.login_id)
            student = Student(user.id, 0, user.name, user.sortable_name, 'None', "", user.login_id, "", 0)
            config.students.append(student)
            student_count += 1
            # if student_count > 100:
            #     break
    # Ophalen Secties en Roles
    print("C05 -", "Ophalen student secties uit Canvas deze koppelen aan Role ")
    canvas_sections = canvas_course.get_sections(include=['students'])
    for course_section in canvas_sections:
        # use only relevant sections
        section = config.find_section(course_section.id)
        if section:
            course_section_students = course_section.students
            if course_section_students:
                for section_student in course_section_students:
                    student_id = section_student["id"]
                    student = config.find_student(student_id)
                    if student:
                        student.role = section.role
                    else:
                        print("C21 -", "Student not found", section_student["id"])
            else:
                print("C22 -", "No students in section", course_section.name)
        else:
            print("C23 -", "Section not found", course_section.name)

    print("C07 -", "Opschonen studenten zonder Role")
    for student in config.students:
        if len(student.role) == 0:
            config.students.remove(student)
    config.student_count = len(config.students)

    # StudentProgress toevoegen aan Students
    for student in config.students:
        student.student_progress = StudentProgress(config.progress.name, config.progress.assignment_groups)
    # Perspectives toevoegen aan Students
    for student in config.students:
        student.perspectives = {}
        for perspective in config.perspectives.values():
            if len(perspective.assignment_groups) > 1:
                # meerdere assignment_group: kennis
                student.perspectives[perspective.name] = StudentPerspective(perspective.name, 0, 0, 0)
                assignment_group_id = config.find_assignment_group_by_role(student.role)
                student.perspectives[perspective.name].assignment_groups.append(assignment_group_id)
            elif len(perspective.assignment_groups) == 1:
                # één assignment_group: team, gilde en peil
                student.perspectives[perspective.name] = StudentPerspective(perspective.name, 0, 0, 0)
                assignment_group_id = config.perspectives[perspective.name].assignment_groups[0]
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
                studentGroup = config.find_student_group(canvas_group.id)
                if studentGroup:
                    canvas_users = canvas_group.get_users()
                    for canvas_user in canvas_users:
                        student = config.find_student(canvas_user.id)
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
                slb_group = config.find_slb_group(canvas_group.id)
                if slb_group:
                    canvas_users = canvas_group.get_users()
                    for canvas_user in canvas_users:
                        student = config.find_student(canvas_user.id)
                        if student:
                            slb_group.students.append(student)
                        else:
                            print("C46 - Student in Canvas slb group not found", canvas_user.id)

        for role in config.roles:
            students = config.find_students_by_role(role.short)
            role.students = students

    # Ophalen Assignments bij de AssignmentsGroups
    canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides', 'online_quiz'])
    for canvas_assignment_group in canvas_assignment_groups:
        # use only relevant assignment_groups
        assignment_group = config.find_assignment_group(canvas_assignment_group.id)
        # print("C61 -", "assignment_group", canvas_assignment_group.id)
        if assignment_group:
            print(f"C62 - assignment_group {assignment_group.name} is used with strategy {assignment_group.strategy}")
            total_group_points = 0
            total_rubrics_points = 0
            for c_assignment in canvas_assignment_group.assignments:
                canvas_assignment = canvas_course.get_assignment(c_assignment['id'], include=['overrides', 'online_quiz'])
                # print("C63 -", canvas_assignment.name, "grading_type:", canvas_assignment.grading_type, "grading_standard_id:", canvas_assignment.grading_standard_id)
                if canvas_assignment.grading_type == "points":
                    points_possible = 0
                    if canvas_assignment.points_possible:
                        total_group_points += canvas_assignment.points_possible
                        points_possible = canvas_assignment.points_possible
                    # print(f"C64 - [{canvas_assignment.grading_type}] points_possible {points_possible}")
                elif canvas_assignment.grading_type == "pass_fail" or canvas_assignment.grading_type == 'letter_grade':
                    points_possible = int(canvas_assignment.points_possible)
                    total_group_points += points_possible
                    # print(f"C65 - {canvas_assignment.grading_type} points_possible {points_possible}")
                else:
                    print(f"C66 - {canvas_assignment.grading_type} AFGEWEZEN grading_type {canvas_assignment.name} points_possible {canvas_assignment.points_possible}")
                    continue
                if canvas_assignment.overrides:
                    for overrides in canvas_assignment.overrides:
                        unlock_date, assignment_date = get_dates(start, overrides)
                        try:
                            section_id = overrides.course_section_id
                        except:
                            section_id = 0
                else:
                    unlock_date, assignment_date = get_dates(start, canvas_assignment)
                    section_id = 0

                assignment = Assignment(canvas_assignment.id, canvas_assignment.name,
                                        canvas_assignment.assignment_group_id, section_id,
                                        canvas_assignment.grading_type, canvas_assignment.grading_standard_id,
                                        points_possible, assignment_date,
                                        unlock_date, date_to_day(start.start_date, assignment_date))
                # print(assignment)
                assignment_group.append_assignment(assignment)
                try:
                    assignment.rubrics, rubrics_points = get_rubrics(canvas_assignment.rubric)
                    if assignment.points > 0 and assignment.points != rubrics_points:
                        print("C75 - ERROR", assignment.name, "assignment points", assignment.points,
                              " points from rubrics",
                              rubrics_points)
                    else:
                        assignment.points = rubrics_points
                        # print("C76 -", assignment.name, "points", assignment.points, "criteria aantal", len(assignment.rubrics))
                    total_rubrics_points += rubrics_points
                except:
                    print("C77 - No rubric", canvas_assignment.name)
                if assignment_group.strategy == "POINTS":
                    assignment_group.total_points = total_group_points
                else:
                    assignment_group.total_points = total_rubrics_points
            print("C78 -", assignment_group.name, "total_group_points", total_group_points, "total_rubrics_points", total_rubrics_points)
            # assignment_group.total_points = group_points_possible
        else:
            print(f"C79 - assignment_group {canvas_assignment_group.name} is not used")

    for student_group in config.student_groups:
        student_group.students = sorted(student_group.students, key=lambda s: s.sortable_name)

    for role in config.roles:
        role.students = sorted(role.students, key=lambda s: s.sortable_name)


    with open(start.course_file_name, 'w') as f:
        dict_result = config.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)


if __name__ == "__main__":
    print("generate_course.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
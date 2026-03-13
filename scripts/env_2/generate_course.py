import json
import sys

from canvasapi import Canvas

from scripts.lib.bandwidth.lib_bandwidth_improved import bandwidth_builder, get_bandwidth_sum, \
    bandwidth_builder_attendance
from scripts.lib.file_const import SECRET_API_KEY_FILE_NAME
from scripts.lib.lib_date import API_URL, get_date_time_obj, date_to_day, get_actual_date
from scripts.lib.file import read_config_from_canvas, read_course, read_secret_api_key, \
    read_dashboard_from_canvas, write_course, read_dashboard
from scripts.lib.lib_student import get_groups, get_section_students, get_students_in_groups, link_students_to_role, \
    link_assessors_to_groups_and_students, link_principal_assessor_to_groups_and_students
from scripts.lib.lib_text import get_extracted_text, get_lu_from_extracted_text
from scripts.model.Assignment import Assignment
from scripts.model.Student import Student
from scripts.model.StudentGroup import StudentGroup
from scripts.model.rubric.Criterion import Criterion
from scripts.model.rubric.Rating import Rating
from scripts.model.attendance.AttendanceMoment import AttendanceMoment


def get_tags(name):
    pos = name.find("(") + 1
    str = name[pos:].strip()
    if str[-1] == ")":
        str = str[:-1]
    tags = str.split()
    return tags


def get_dates(config, canvas_object):
    if canvas_object.due_at:
        assignment_date = get_date_time_obj(canvas_object.due_at)
    else:
        if canvas_object.lock_at:
            assignment_date = get_date_time_obj(canvas_object.lock_at)
        else:
            assignment_date = config.end_date
    if canvas_object.unlock_at:
        unlock_date = get_date_time_obj(canvas_object.unlock_at)
    else:
        unlock_date = config.start_date
    return unlock_date, assignment_date


def get_rubrics(canvas_rubrics):
    # print("C74 -", canvas_assignment)
    rubrics_points = 0
    rubrics = []
    for canvas_criterium in canvas_rubrics:
        criterion = Criterion(canvas_criterium['id'], canvas_criterium['points'], canvas_criterium['description'])
        # print("GC71 -", criterion)
        rubrics_points += criterion.points
        rubrics.append(criterion)
        for canvas_rating in canvas_criterium['ratings']:
            criterion.ratings.append(Rating(canvas_rating['id'], canvas_rating['points'], canvas_rating['description']))
    return rubrics, rubrics_points


def get_used_assignment_groups(config):
    used_assignment_groups = []
    if config.level_moments is not None:
        if len(config.level_moments.assignment_group_ids) > 0:
            used_assignment_groups += config.level_moments.assignment_group_ids
        else:
            message = "GC01 - WARNING no assignments_group for level_moments perspective " + config.level_moments.name
            print(message)
    else:
        print("GC03 - NO level_moments perspective ")

    if config.grade_moments is not None:
        if len(config.grade_moments.assignment_group_ids) > 0:
            used_assignment_groups += config.grade_moments.assignment_group_ids
        else:
            message = "GC05 - WARNING no assignments_group for grade_moments perspective " + config.grade_moments.name
            print(message)
    else:
        print("GC07 - NO level_moments perspective ")

    for perspective in config.perspectives.values():
        if len(perspective.assignment_group_ids) > 0:
            used_assignment_groups += perspective.assignment_group_ids
        else:
            message = "GC09 - WARNING no assignments_group for perspective ", perspective.name
            print(message)

    print("GC11 - Used assignment_groups", used_assignment_groups)
    return used_assignment_groups


def get_attendance(attendance):
    starting_days = attendance.policy.starting_days
    if len(starting_days) == 0:
        message = "GC81 - ERROR - Geen starting_days opgegeven in attendance.policy"
        print(message)
        return None
    if "WEEKLY" not in attendance.policy.recurring:
        message = f"GC81 - ERROR - Ongeldige recurring [{attendance.policy.recurring}] opgegeven in attendance.policy"
        print(message)
        return None
    if len(starting_days) == 1:
        moments = []
        for week in range(0, attendance.policy.times):
            if week+1 in attendance.policy.exceptions:
                continue
            day = starting_days[0] + week*7
            points = 2
            moment = AttendanceMoment(day, points)
            # print(day, moment)
            attendance.attendance_moments.append(moment)
    return attendance

def get_predefined_lu(course, assignment_sequence, assignment):
    print("GCRS51 -", assignment.name)
    if "@" in assignment.name:
        print("GCRS52 -", assignment.name)
        lu_list = get_lu_from_extracted_text(assignment.name)
        print("GCRS53 -", len(lu_list))
        assignment.learning_outcomes.extend(lu_list)
        # assignment.name = text_list[0]["text"]
        print("GCRS54 -", assignment.name, assignment.learning_outcomes)
        for lu in assignment.learning_outcomes:
            # establish many-2-many relation
            learning_outcome = course.find_learning_outcome(lu)
            if learning_outcome is not None:
                # print("GC53 -", assignment.name, "LU:", learning_outcome.id)
                learning_outcome.add_assignment_tag_id(assignment_sequence.tag)
                assignment_sequence.learning_outcomes.append(learning_outcome.id)
    for criterium in assignment.rubrics:
        # print("GC55 -", criterium.description)
        if "@" in criterium.description:
            feedback_list = get_extracted_text(criterium.description)
            criterium.learning_outcomes.append(feedback_list[0]["lu"])
            criterium.description = feedback_list[0]["text"]
            # print("GC56 -", criterium.learning_outcomes, criterium.description)
            for learning_outcome_id in criterium.learning_outcomes:
                # print("GC91 -", learning_outcome_id)
                # establish many-2-many relation
                learning_outcome = course.find_learning_outcome(learning_outcome_id)
                if learning_outcome is not None:
                    learning_outcome.add_criterion_id(assignment_sequence.tag, criterium.id)
                    assignment_sequence.add_learning_outcome(learning_outcome_id)
                    assignment.add_learning_outcome(learning_outcome_id)


def generate_course(course_instance):
    print("GCS01 - generate_course.py")
    g_actual_date = get_actual_date()
    secret_api_key = read_secret_api_key(SECRET_API_KEY_FILE_NAME)
    canvas = Canvas(API_URL, secret_api_key.canvas_api_key)
    canvas_course = canvas.get_course(course_instance.canvas_course_id)

    if course_instance.stage == "PROD":
        config = read_config_from_canvas(canvas_course)
        dashboard = read_dashboard_from_canvas(canvas_course)
    else:
        config = read_course(course_instance.get_config_file_name())
        dashboard = read_dashboard(course_instance.get_dashboard_file_name())

    # with open(course_instance.get_config_file_name(), "w", encoding="utf-8") as file:
    #     dict_result = config.to_json()
    #     json.dump(dict_result, file, ensure_ascii=False, indent=2)

    user = canvas.get_current_user()
    print("GCS03 -", user.name)
    if config.attendance is not None:
        attendance = get_attendance(config.attendance)
        if attendance is not None:
            config.attendance = attendance

    uses_assignment_groups = get_used_assignment_groups(config)

    # Ophalen Assignments bij de AssignmentsGroups
    canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides', 'online_quiz'])
    for canvas_assignment_group in canvas_assignment_groups:
        # use only relevant assignment_groups
        assignment_group = config.get_assignment_group(canvas_assignment_group.id)
        # print("GC21 -", "assignment_group", canvas_assignment_group.id)

        if assignment_group and (assignment_group.id in uses_assignment_groups):
            tags = []
            print(f"GCS22 - assignment_group {assignment_group.name} is used with strategy {assignment_group.strategy}")
            for c_assignment in canvas_assignment_group.assignments:
                message = ""
                canvas_assignment = canvas_course.get_assignment(c_assignment['id'], include=['overrides', 'online_quiz'])
                str_print = f"GC23 - {canvas_assignment.name} grading_type [{canvas_assignment.grading_type}] grading_standard_id [{canvas_assignment.grading_standard_id}]"
                print(str_print)
                points_possible = 0
                sections = []
                if canvas_assignment.grading_type == "points":
                    if canvas_assignment.points_possible:
                        points_possible = canvas_assignment.points_possible
                    else:
                        print(f"GCS64 - WARNING [{canvas_assignment.grading_type}] points_possible is not set for", canvas_assignment.name)
                elif canvas_assignment.grading_type == "pass_fail":
                    points_possible = canvas_assignment.points_possible
                elif canvas_assignment.grading_type == 'letter_grade':
                    if canvas_assignment.points_possible:
                        points_possible = canvas_assignment.points_possible
                    else:
                        message = f"GCS65 - WARNING [{canvas_assignment.grading_type}] points_possible is not set for", canvas_assignment.name
                        print(message)
                else:
                    message = f"GCS26 - ERROR - {canvas_assignment.grading_type} AFGEWEZEN grading_type {canvas_assignment.name} points_possible {canvas_assignment.points_possible}"
                    print(message)
                    continue
                if canvas_assignment.overrides:
                    new_assignment_date = config.start_date
                    for overrides in canvas_assignment.overrides:
                        unlock_date, assignment_date = get_dates(config, overrides)
                        if assignment_date > new_assignment_date:
                            new_assignment_date = assignment_date
                        if hasattr(overrides, "course_section_id"):
                            section_id = overrides.course_section_id
                            sections.append(overrides.course_section_id)
                        else:
                            section_id = 0
                else:
                    unlock_date, new_assignment_date = get_dates(config, canvas_assignment)
                    section_id = 0

                assignment = Assignment(canvas_assignment.id, canvas_assignment.name,
                                        canvas_assignment.assignment_group_id, section_id,
                                        canvas_assignment.grading_type, canvas_assignment.grading_standard_id,
                                        points_possible, canvas_assignment.submission_types, new_assignment_date,
                                        unlock_date, date_to_day(config.start_date, new_assignment_date), date_to_day(config.start_date, unlock_date))
                assignment.sections = sections
                if len(message) > 0:
                    assignment.messages.append(message)
                # print(assignment)
                tag_sequence = str(assignment.id)
                if "#" in assignment.name:
                    tags = get_tags(assignment.name)
                    for t in tags:
                        # print("GC60 -", t)
                        if "#" in t[0]:
                            tag_sequence = t[1:]
                            break

                if assignment.grading_type == "pass_fail":
                    if hasattr(canvas_assignment, "rubric"):
                        # gebruik de punten uit de rubrics
                        assignment.rubrics, rubrics_points = get_rubrics(canvas_assignment.rubric)
                        # print("GC31 - ",len(assignment.rubrics))
                        if assignment.points > 0 and assignment.points != rubrics_points:
                            message = f"GCS33 - ERROR inconsistency in assignment {assignment.name} assignment points {assignment.points} rubrics points {rubrics_points}"
                            assignment.messages.append(message)
                            print(message)
                        else:
                            if rubrics_points > 0:
                                assignment.points = rubrics_points
                    else:
                        print("GC34 - INFO No rubric", assignment.name, "grading_type", assignment.grading_type)
                        if assignment.points == 0:
                            assignment.points = 2

                elif assignment.grading_type == "letter_grade":
                    if hasattr(canvas_assignment, "rubric"):
                        assignment.rubrics, rubrics_points = get_rubrics(canvas_assignment.rubric)

                        # print("GC31 - ",len(assignment.rubrics))
                        if assignment.points > 0 and assignment.points != rubrics_points:
                            message = f"GCS33 - WARNING inconsistency in assignment {assignment.name} assignment points {assignment.points} rubrics points {rubrics_points}"
                            assignment.messages.append(message)
                            print(message)
                        else:
                            if rubrics_points > 0:
                                assignment.points = rubrics_points
                    else:
                        message = f"GCS34 - WARNING No rubric in assignment {assignment.name} grading_type {assignment.grading_type}"
                        assignment.messages.append(message)
                        print(message)
                elif assignment.grading_type == "points":
                    if hasattr(canvas_assignment, "rubric"):
                        assignment.rubrics, rubrics_points = get_rubrics(canvas_assignment.rubric)
                        if assignment.points > 0 and assignment.points != rubrics_points:
                            message = f"GCS36 - WARNING inconsistency in assignment {assignment.name} assignment points {assignment.points} rubrics points {rubrics_points}"
                            assignment.messages.append(message)
                            print(message)
                        else:
                            if rubrics_points > 0:
                                assignment.points = rubrics_points
                    else:
                        if "external_tool" in canvas_assignment.submission_types:
                            pass
                        else:
                            message = f"GCS38 - WARNING No rubric in assignment {assignment.name} grading_type {assignment.grading_type}"
                            assignment.messages.append(message)
                            print(message)
                else:
                    message = f"GCS40 - ERROR Unsupported grading_type {assignment.grading_type}"
                    assignment.messages.append(message)
                    print(message)
                assignment_group.append_assignment(tag_sequence, assignment)

            total_group_points = 0
            for assignment_sequence in assignment_group.assignment_sequences:
                # Filter de verbeteropdrachten er uit
                if "Verbeter" in assignment_sequence.name:
                    continue
                elif assignment_sequence.get_day() > (config.days_in_semester - config.improvement_period):
                    print("GCS49 - assigment_date ligt in verbeterperiode", assignment_sequence.name, assignment_sequence.get_day())
                    continue
                elif "Aanvullend" in assignment_sequence.name:
                    continue
                else:
                    total_group_points += assignment_sequence.points
            assignment_group.total_points = total_group_points
            # print("GC47 -", tags_lu)
            print("GCS51 -", assignment_group.name, "punten:", assignment_group.total_points)
        else:
            print(f"GCS41 - assignment_group {canvas_assignment_group.name} is not used")

    for perspective in config.perspectives:
        for assignment_group_id in config.perspectives[perspective].assignment_group_ids:
            assignment_group = config.get_assignment_group(assignment_group_id)
            if assignment_group:
                print("GCS71 -", assignment_group.name)
                for assignment_sequence in assignment_group.assignment_sequences:
                    for assignment in assignment_sequence.assignments:
                        get_predefined_lu(config, assignment_sequence, assignment)
                    # config.perspectives[perspective].assignment_sequences.append(assignment_sequence)
            else:
                print("GCS72 - ERROR", assignment_group_id, "not found in config perspective", perspective)

    for assignment_group_id in config.level_moments.assignment_group_ids:
        assignment_group = config.get_assignment_group(assignment_group_id)
        print("GCS73 -", assignment_group.name)
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                get_predefined_lu(config, assignment_sequence, assignment)

    for assignment_group_id in config.grade_moments.assignment_group_ids:
        assignment_group = config.get_assignment_group(assignment_group_id)
        print("GCS73 -", assignment_group.name)
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                get_predefined_lu(config, assignment_sequence, assignment)

    for assignment_group in config.assignment_groups:
        assignment_group.assignment_sequences = sorted(assignment_group.assignment_sequences, key=lambda a: a.get_day())
        print("GS101 -", assignment_group.name, assignment_group.strategy)
        assignment_group.bandwidth = bandwidth_builder(assignment_group, config.days_in_semester)

    for perspective_key in config.perspectives:
        config.perspectives[perspective_key].assignment_sequences = sorted(config.perspectives[perspective_key].assignment_sequences, key=lambda a: a.get_day())
        config.perspectives[perspective_key].bandwidth = get_bandwidth_sum(config, config.perspectives[perspective_key].assignment_group_ids)
        config.perspectives[perspective_key].total_points = 0
        for assignment_sequence in config.perspectives[perspective_key].assignment_sequences:
            config.perspectives[perspective_key].total_points += assignment_sequence.points
    if config.attendance is not None:
        config.attendance.bandwidth = bandwidth_builder_attendance(config.attendance.lower_points, config.attendance.upper_points, config.attendance.total_points, config.days_in_semester)

    # Ophalen Students
    print("GS005 - Retrieve students")
    config.students = []
    canvas_users = canvas_course.get_users(enrollment_type=['student'], include=["enrollments"])
    for canvas_user in canvas_users:
        if hasattr(canvas_user, 'login_id'):
            print("GST007 - Create student", canvas_user.login_id, canvas_user.name, canvas_user.sis_user_id)
            student = Student(canvas_user.id, 0, 0, canvas_user.name, canvas_user.sis_user_id, canvas_user.sortable_name, "", canvas_user.login_id, "")
            config.students.append(student)
        else:
            if hasattr(canvas_user, 'sis_user_id'):
                print("GST008 - Create student without login_id", canvas_user.name, canvas_user.sis_user_id)
                student = Student(canvas_user.id, 0, 0, canvas_user.name, canvas_user.sis_user_id, canvas_user.sortable_name, "", "", "")
                # print("GS17 ", student)
                config.students.append(student)
    print("GCRS20 - Aantal studenten", len(config.students))
    # for student in course.students:
    #     print("GST010 -", student)
    if dashboard.project_group_name == "SECTIONS":
        group_list = []
        print("GCRS21 - Werken met Canvas secties als groepen (meestal S1 propedeuse).")
        for section in config.sections:
            print("GCRS22 -", section)
            student_group = StudentGroup(section.id, section.name, 0)
            group_list.append(student_group)
    else:
        group_list = get_groups(dashboard.project_group_name, canvas_course)
    config.project_groups = group_list
    config.guild_groups = get_groups(dashboard.guild_group_name, canvas_course)
    get_section_students(dashboard.project_group_name, config, canvas_course)

    if dashboard.project_group_name == "SECTIONS":
        print("GCRS31 - Werken met Canvas secties als groepen (meestal S1 propedeuse).")
    else:
        get_students_in_groups(dashboard.project_group_name, config, canvas_course)
    if len(dashboard.guild_group_name) >0 :
        get_students_in_groups(dashboard.guild_group_name, config, canvas_course)
    link_students_to_role(config)
    link_assessors_to_groups_and_students(config)
    link_principal_assessor_to_groups_and_students(config)

    print("GCRS72 - Opschonen studenten zonder Role, totaal", len(config.students))
    without_role = 0
    course_students = config.students.copy()
    for student in course_students:
        # print("GST23 -", student.name, "["+student.role+"]")
        if len(student.role) == 0:
            print("GCRS73 - Verwijder student uit lijst, heeft geen role", student.name)
            config.remove_student(student.id)
            without_role += 1
    print("GCRS74 - Opschonen studenten zonder ProjectGroup")
    course_students = config.students.copy()
    without_project = 0
    for student in course_students:
        # print("GST014 -", student.name, "["+student.role+"]")
        if student.project_id == 0:
            print("GST015 - Verwijder student uit lijst, heeft geen project", student.name)
            config.remove_student(student.id)
            without_project += 1

    config.student_count = len(config.students)

    for student_group in config.project_groups:
        student_group.students = sorted(student_group.students, key=lambda s: s.sortable_name)
    for student_group in config.guild_groups:
        student_group.students = sorted(student_group.students, key=lambda s: s.sortable_name)
    for role in config.roles:
        role.students = sorted(role.students, key=lambda s: s.sortable_name)

    print("GCRS80 - Aantal Canvas studenten", len(config.students))
    # for student in course.students:
    #     print("GST017 -", student)

    write_course(course_instance.get_course_file_name(), config)

    print("GCRS99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_course(sys.argv[1], sys.argv[2])
    else:
        generate_course("", "")

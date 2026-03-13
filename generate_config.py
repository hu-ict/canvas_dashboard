import sys
from canvasapi import Canvas
import json
from scripts.lib.bandwidth.lib_bandwidth import IMPROVEMENT_PERIOD
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, SECRET_API_KEY_FILE_NAME
from scripts.lib.lib_date import API_URL, get_actual_date, get_date_time_obj
from scripts.lib.file import read_dashboard_from_canvas, read_environment, read_secret_api_key, read_dashboard
from scripts.lib.lib_student import get_groups
from scripts.lib.lib_trm import generate_trm
from scripts.model.AssignmentGroup import AssignmentGroup
from scripts.model.Bandwidth import Bandwidth
from scripts.model.CourseConfig import CourseConfig
from scripts.model.Role import Role
from scripts.model.Section import Section
from scripts.model.StudentGroup import StudentGroup
from scripts.model.teacher.Teacher import Teacher
from scripts.model.attendance.Attendance import Attendance
from scripts.model.moment.GradeMoments import GradeMoments
from scripts.model.moment.LevelMoments import LevelMoments
from scripts.model.perspective.Perspective import Perspective
from scripts.model.attendance.Policy import Policy


def generate_config(instance_name):
    print("GCF01 - generate_config.py")
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    secret_api_key = read_secret_api_key(SECRET_API_KEY_FILE_NAME)
    current_instance = environment.get_instance_of_course(environment.current_instance)
    print("Instance:", current_instance.name)
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, secret_api_key.canvas_api_key)
    user = canvas.get_current_user()
    print(user.name)
    canvas_course = canvas.get_course(current_instance.canvas_course_id)
    if current_instance.stage == "DEV":
        dashboard = read_dashboard(current_instance.get_dashboard_file_name())
    else:
        dashboard = read_dashboard_from_canvas(canvas_course)
    print("GCF11 - course_instance.course_code", current_instance.course_code)

    config = CourseConfig(current_instance.course_code, current_instance.canvas_course_id, canvas_course.name,
                          get_date_time_obj(current_instance.period["start_date"]),
                          get_date_time_obj(current_instance.period["end_date"]),
                          IMPROVEMENT_PERIOD,
                          0, 0, 0)
    if len(dashboard.roles) > 1:
        config.roles = dashboard.roles
    if len(dashboard.learning_outcomes) > 0:
        config.learning_outcomes = dashboard.learning_outcomes
    print("GCNF20 -", dashboard.assignment_groups)
    for perspective in dashboard.perspectives:
        if len(perspective.assignment_group_names) > 0:
            print("GCNF21 -", perspective.assignment_group_names)

            # retrieve assignments_groups and score
            canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides'])
            for canvas_assignment_group in canvas_assignment_groups:
                meta_assignment_group = dashboard.get_assignment_group_by_name(canvas_assignment_group.name)
                print("GCNF24 - assignment_group", canvas_assignment_group.name, meta_assignment_group)
                if meta_assignment_group:
                    assignment_group = AssignmentGroup(canvas_assignment_group.id, canvas_assignment_group.name,
                                                       meta_assignment_group.groups, meta_assignment_group.strategy,
                                                       meta_assignment_group.lower_c,
                                                       meta_assignment_group.upper_c,
                                                       meta_assignment_group.total_points,
                                                       meta_assignment_group.lower_points,
                                                       meta_assignment_group.upper_points,
                                                       meta_assignment_group.levels, meta_assignment_group.marker)
                    for canvas_assignment in canvas_assignment_group.assignments:
                        if canvas_assignment['points_possible']:
                            assignment_group.total_points += canvas_assignment['points_possible']
                    print("GCNF25 - assignment_group", canvas_assignment_group, "points", meta_assignment_group.total_points, assignment_group.total_points,
                          assignment_group.strategy)
                    config.assignment_groups.append(assignment_group)
                else:
                    print("GCNF27 - assignment_group wordt niet gebruikt", canvas_assignment_group.name)
            print("GCNF26 - assignment_groups", len(config.assignment_groups))

    if dashboard.level_moments:
        print("GCNF31 -", dashboard.level_moments)
        config.level_moments = LevelMoments("level_moments", dashboard.level_moments.title)
        for assignment_group_name in dashboard.level_moments.assignment_group_names:
            assignment_group = config.find_assignment_group_by_name(assignment_group_name)
            print("GCNF32 -", assignment_group_name, assignment_group)
            if assignment_group:
                config.level_moments.assignment_group_ids.append(assignment_group.id)
        print("GCNF33 -", config.level_moments)
    if dashboard.grade_moments:
        print("GCNF41 -", dashboard.grade_moments)
        config.grade_moments = GradeMoments("grade_moments", dashboard.grade_moments.title)
        for assignment_group_name in dashboard.grade_moments.assignment_group_names:
            assignment_group = config.find_assignment_group_by_name(assignment_group_name)
            print("GCNF42 -", assignment_group_name, assignment_group)
            if assignment_group:
                config.grade_moments.assignment_group_ids.append(assignment_group.id)
        print("GCNF43 -", config.grade_moments)
    for meta_perspective in dashboard.perspectives:
        print("GCNF51 -", meta_perspective.name)
        perspective = Perspective(meta_perspective.name, meta_perspective.title, meta_perspective.show_flow,
                                  meta_perspective.show_points, 0)
        for assignment_group_name in meta_perspective.assignment_group_names:
            assignment_group = config.find_assignment_group_by_name(assignment_group_name)
            if assignment_group:
                perspective.assignment_group_ids.append(assignment_group.id)
        config.perspectives[perspective.name] = perspective
    if current_instance.course_code in ["TICT-V1SE1-24"]:
        role = Role("role", "Student", "HBO-ICT", "border-dark")
        config.roles.append(role)
        # policy = Policy([1], "WEEKLY", 19, [9, 17, 18])
        # config.attendance = Attendance("attendance", "Aanwezigheid", "attendance", True, False, "ATTENDANCE", 100, 75,
        #                               90, Bandwidth(), policy)
    config.project_principal_assignment_group_id = config.find_assignment_group_by_name(dashboard.project_principal_assignment_group).id
    config.guild_principal_assignment_group_id = config.find_assignment_group_by_name(dashboard.guild_principal_assignment_group).id

    # ophalen secties
    course_sections = canvas_course.get_sections()
    for course_section in course_sections:
        if current_instance.course_code in ["TICT-V3SE5-25", "TICT-V3SE6-25"]:
            new_section = Section(course_section.id, course_section.name, course_section.name)
        else:
            new_section = Section(course_section.id, course_section.name, "role")
        config.sections.append(new_section)
        print("GCNF62 - course_section", new_section)

    # retrieve Teachers
    canvas_users = canvas_course.get_users(enrollment_type=['teacher', 'ta'])
    teacher_count = 0
    for canvas_user in canvas_users:
        teacher_count += 1

        if hasattr(canvas_user, 'email'):
            teacher = Teacher(canvas_user.id, canvas_user.name, canvas_user.email)
            # print("GCONF15 - Create teacher with email", canvas_user.email)
        else:
            teacher = Teacher(canvas_user.id, canvas_user.name, "")
            print("GCNF72 - Create teacher without email", canvas_user.name)
        config.teachers.append(teacher)
        print("GCNF73 -", teacher)
    # opschonen van sections"
    for section in config.sections[:]:  # kopie met slicing
        yes_no = input(f"Section behouden {section.name} [enter or n]")
        if 'n' in yes_no.lower():
            print(f"GCNF81 - Verwijder section {section.name}")
            config.sections.remove(section)

    if dashboard.project_group_name == "SECTIONS":
        group_list = []
        print("GCNF91 - Werken met Canvas secties als groepen (meestal S1 propedeuse).")
        for section in config.sections:
            print("GCNF92 -", section)
            student_group = StudentGroup(section.id, section.name, 0)
            group_list.append(student_group)
    else:
        group_list = get_groups(dashboard.project_group_name, canvas_course)
    config.project_groups = group_list
    if len(dashboard.guild_group_name) > 0:
        group_list = get_groups(dashboard.guild_group_name, canvas_course)
        config.guild_groups = group_list


    # opschonen van assignment_groups zonder revelantie
    print("GCNF95 - config.assignment_groups", len(config.assignment_groups))
    for assignment_group in config.assignment_groups[:]:  # kopie met slicing
        yes_no = input(f"assignment_group behouden {assignment_group.name} [enter or n]")
        if yes_no == 'n':
            print(f"GCNF96 - Verwijder assignment_group {assignment_group.name}")
            config.assignment_groups.remove(assignment_group)

    print("GCONF98 - ConfigFileName:", current_instance.get_config_file_name())
    with open(current_instance.get_config_file_name(), 'w') as f:
        dict_result = config.to_json()
        json.dump(dict_result, f, indent=2)

    generate_trm(current_instance, config)

    print("GCONF99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_config(sys.argv[1])
    else:
        generate_config("")

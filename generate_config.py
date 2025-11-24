import sys

from canvasapi import Canvas
import json

from generate_students import get_groups
from lib.lib_bandwidth import IMPROVEMENT_PERIOD
from lib.lib_date import API_URL, date_to_day, get_actual_date
from lib.file import read_start, read_course_instances, read_dashboard_from_canvas
from model.AssignmentGroup import AssignmentGroup
from model.Bandwidth import Bandwidth
from model.CourseConfig import CourseConfig
from model.Role import Role
from model.Section import Section
from model.teacher.Teacher import Teacher
from model.attendance.Attendance import Attendance
from model.moment.GradeMoments import GradeMoments
from model.moment.LevelMoments import LevelMoments
from model.perspective.Perspective import Perspective
from model.attendance.Policy import Policy


def generate_config(instance_name):
    print("GCF01 - generate_config.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("Instance:", instance.name)
    start = read_start(instance.get_start_file_name())
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print(user.name)
    canvas_course = canvas.get_course(start.canvas_course_id)
    dashboard = read_dashboard_from_canvas(canvas_course)

    config = CourseConfig(start.canvas_course_id, canvas_course.name,
                          start.start_date,
                          start.end_date,
                          date_to_day(start.start_date, start.end_date),
                          IMPROVEMENT_PERIOD,
                          0, 0)
    if len(dashboard.roles) > 1:
        config.roles = dashboard.roles
    if len(dashboard.learning_outcomes) > 1:
        config.learning_outcomes = dashboard.learning_outcomes
    if len(dashboard.assignment_groups) > 0:
        # retrieve assignments_groups and score
        canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides'])
        for canvas_assignment_group in canvas_assignment_groups:
            meta_assignment_group = dashboard.get_assignment_group_by_name(canvas_assignment_group.name)
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
                print("GC05 - assignment_group", canvas_assignment_group, "points", meta_assignment_group.total_points, assignment_group.total_points,
                      assignment_group.strategy)
                config.assignment_groups.append(assignment_group)

    for meta_perspective in dashboard.perspectives:
        if meta_perspective.name == "level_moments":
            config.level_moments = LevelMoments("level_moments", meta_perspective.title)
            for assignment_group_name in meta_perspective.assignment_group_names:
                assignment_group = config.find_assignment_group_by_name(assignment_group_name)
                if assignment_group:
                    config.level_moments.assignment_group_ids.append(assignment_group.id)
        elif meta_perspective.name == "grade_moments":
            config.grade_moments = GradeMoments("grade_moments", meta_perspective.title)
            for assignment_group_name in meta_perspective.assignment_group_names:
                assignment_group = config.find_assignment_group_by_name(assignment_group_name)
                if assignment_group:
                    config.grade_moments.assignment_group_ids.append(assignment_group.id)
        else:
            perspective = Perspective(meta_perspective.name, meta_perspective.title, meta_perspective.show_flow,
                                      meta_perspective.show_points, 0)
            for assignment_group_name in meta_perspective.assignment_group_names:
                assignment_group = config.find_assignment_group_by_name(assignment_group_name)
                if assignment_group:
                    perspective.assignment_group_ids.append(assignment_group.id)
            config.perspectives[perspective.name] = perspective
    if instance.is_instance_of("courses_2026"):
        config.attendance = None
    else:
        role = Role("role", "Student", "HBO-ICT", "border-dark")
        config.roles.append(role)
        perspective = Perspective("kennis", "Kennis", True, False, 0)
        config.perspectives[perspective.name] = perspective
        perspective = Perspective("verbreding", "Oriëntatie", True, False, 0)
        config.perspectives[perspective.name] = perspective
        perspective = Perspective("skills", "Professional skills", True, False, 0)
        config.perspectives[perspective.name] = perspective
        policy = Policy([1], "WEEKLY", 19, [9, 17, 18])
        config.attendance = Attendance("attendance", "Aanwezigheid", "attendance", True, False, "ATTENDANCE", 100, 75,
                                      90, Bandwidth(), policy)
        config.level_moments = LevelMoments("level_moments", "Peilmomenten", "progress",
                                            ["Peilmoment 1", "Peilmoment 2"])
        config.grade_moments = GradeMoments("grade_moments", "Beoordelingsmomenten", "grade",
                                        ["Semester-beslissing", "Semester-eindbeslissing"])

    # ophalen secties
    course_sections = canvas_course.get_sections()
    for course_section in course_sections:
        if instance.is_instance_of("courses_2026"):
            new_section = Section(course_section.id, course_section.name, course_section.name)
        else:
            new_section = Section(course_section.id, course_section.name, "role")
        config.sections.append(new_section)
        print("GCONF08 - course_section", new_section)

    # retrieve assignments_groups and score
    # canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides'])
    # for canvas_assignment_group in canvas_assignment_groups:
    #     assignment_group = AssignmentGroup(canvas_assignment_group.id, canvas_assignment_group.name, "project", "POINTS",
    #                                        0, 0, 0, 0, 0, "level", "circle")
    #     for canvas_assignment in canvas_assignment_group.assignments:
    #         if canvas_assignment['points_possible']:
    #             assignment_group.total_points += canvas_assignment['points_possible']
    #     print("GC05 - assignment_group", canvas_assignment_group, "points", assignment_group.total_points, assignment_group.strategy)
    #     config.assignment_groups.append(assignment_group)

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
            print("GCONF16 - Create teacher without email", canvas_user.name)
        config.teachers.append(teacher)
        print("GCONF18 -", teacher)


    group_list = get_groups(start.project_group_name, canvas_course)
    config.project_groups = group_list
    group_list = get_groups(start.guild_group_name, canvas_course)
    config.guild_groups = group_list

    print("GCONF98 - ConfigFileName:", instance.get_config_file_name())
    with open(instance.get_config_file_name(), 'w') as f:
        dict_result = config.to_json()
        json.dump(dict_result, f, indent=2)

    print("GCONF99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_config(sys.argv[1])
    else:
        generate_config("")

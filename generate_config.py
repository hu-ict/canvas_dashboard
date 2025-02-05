import sys

from canvasapi import Canvas
import json

from lib.lib_bandwidth import IMPROVEMENT_PERIOD
from lib.lib_date import API_URL, get_date_time_obj, date_to_day, get_actual_date
from lib.file import read_start, read_course_instances
from model.Assignment import Assignment
from model.AssignmentGroup import AssignmentGroup
from model.Bandwidth import Bandwidth
from model.CourseConfig import CourseConfig
from model.Role import Role
from model.Section import Section
from model.StudentGroup import StudentGroup
from model.Teacher import Teacher
from model.instance.CourseInstances import CourseInstances
from model.perspective.Attendance import Attendance
from model.perspective.GradeMoments import GradeMoments
from model.perspective.LevelMoments import LevelMoments
from model.perspective.Perspective import Perspective
from model.perspective.Policy import Policy


def generate_config(instance_name):
    print("GCF01 - generate_config.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("Instance:", instance.name)
    start1 = read_start(instance.get_start_file_name())
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start1.api_key)
    user = canvas.get_current_user()
    print(user.name)
    canvas_course = canvas.get_course(start1.canvas_course_id)

    config = CourseConfig(start1.canvas_course_id, canvas_course.name,
                          start1.start_date,
                          start1.end_date,
                          date_to_day(start1.start_date, start1.end_date),
                          IMPROVEMENT_PERIOD,
                          0)

    if instance.is_instance_of("inno_courses"):
        role = Role("AI", "AI - Engineer", "Artificial Intelligence", "border-warning")
        config.roles.append(role)
        role = Role("BIM", "Business Analist", "Business and IT Management", "border-success")
        config.roles.append(role)
        role = Role("CSC_C", "Cloud", "Cyber Security and Cloud", "border-light")
        config.roles.append(role)
        role = Role("CSC_S", "Security", "Cyber Security and Cloud", "border-danger")
        config.roles.append(role)
        role = Role("SD_B", "Back-end developer", "Software Development", "border-dark")
        config.roles.append(role)
        role = Role("SD_F", "Front-end developer", "Software Development", "border-primary")
        config.roles.append(role)
        role = Role("TI", "TI - Engineer", "Technische Informatica", "border-warning")
        config.roles.append(role)
        perspective = Perspective("team", "Team", "samen", False, True)
        config.perspectives[perspective.name] = perspective
        perspective = Perspective("gilde", "Gilde", "samen5", False, True)
        config.perspectives[perspective.name] = perspective
        perspective = Perspective("kennis", "Kennis", "niveau", True, False)
        config.perspectives[perspective.name] = perspective
        config.attendance = None
        config.level_moments = LevelMoments("level_moments", "Peilmomenten", "progress", ["Sprint 4", "Sprint 7"])
        config.grade_moments = GradeMoments("grade_moments", "Beoordelingsmomenten", "grade", ["Beoordeling"])
    else:
        role = Role("role", "Student", "HBO-ICT", "border-dark")
        config.roles.append(role)
        perspective = Perspective("kennis", "Kennis", "bin2", True, False)
        config.perspectives[perspective.name] = perspective
        perspective = Perspective("verbreding", "Kennis", "bin2", True, False)
        config.perspectives[perspective.name] = perspective
        perspective = Perspective("skills", "Professional shills", "bin2", True, False)
        config.perspectives[perspective.name] = perspective
        policy = Policy([1], "WEEKLY", 19, [9, 17, 18])
        config.attendance = Attendance("attendance", "Aanwezigheid", "attendance", True, False, "ATTENDANCE", 100, 75,
                                      90, Bandwidth(), policy)
        config.level_moments = LevelMoments("level_moments", "Peilmomenten", "progress",
                                            ["Peilmoment 1", "Peilmoment 2"],)
        config.grade_moments = GradeMoments("grade_moments", "Beoordelingsmomenten", "grade",
                                        ["Semester-beslissing", "Semester-eindbeslissing"], )

    # ophalen secties
    course_sections = canvas_course.get_sections()
    for course_section in course_sections:
        new_section = Section(course_section.id, course_section.name, "role")
        config.sections.append(new_section)
        if start1.projects_groep_name == "SECTIONS":
            new_student_group = StudentGroup(new_section.id, new_section.name)
            config.student_groups.append(new_student_group)
        print("course_section", new_section)

    # retrieve assignments_groups and score
    canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides'])
    for canvas_assignment_group in canvas_assignment_groups:
        assignment_group = AssignmentGroup(canvas_assignment_group.id, canvas_assignment_group.name, [], "POINTS",
                                           0, 0, 0, 0, 0, None)
        for canvas_assignment in canvas_assignment_group.assignments:
            if canvas_assignment['points_possible']:
                assignment_group.total_points += canvas_assignment['points_possible']
        print("GC05 assignment_group", canvas_assignment_group, "points", assignment_group.total_points, assignment_group.strategy)
        config.assignment_groups.append(assignment_group)

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
        print("GCONF18", teacher)

    canvas_group_categories = canvas_course.get_group_categories()
    for canvas_group_category in canvas_group_categories:
        print(canvas_group_category)
        # retrieve project_groups
        if canvas_group_category.name == start1.projects_groep_name:
            canvas_groups = canvas_group_category.get_groups()
            for canvas_group in canvas_groups:
                studentGroup = StudentGroup(canvas_group.id, canvas_group.name)
                config.student_groups.append(studentGroup)
                print(canvas_group)

    config.learning_outcomes = []
    print("GC98 - ConfigFileName:", instance.get_config_file_name())
    with open(instance.get_config_file_name(), 'w') as f:
        dict_result = config.to_json()
        json.dump(dict_result, f, indent=2)

    print("GC99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_config(sys.argv[1])
    else:
        generate_config("")

import sys

from canvasapi import Canvas
import json
from lib.lib_date import API_URL, get_date_time_obj, date_to_day, get_actual_date
from lib.file import read_start, read_course_instance
from model.Assignment import Assignment
from model.AssignmentGroup import AssignmentGroup
from model.CourseConfig import CourseConfig
from model.Section import Section
from model.StudentGroup import StudentGroup
from model.Teacher import Teacher
from model.instance.CourseInstances import CourseInstances


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print(user.name)
    canvas_course = canvas.get_course(start.canvas_course_id)
    course_config = CourseConfig(canvas_course.name, date_to_day(start.start_date, start.end_date), 0)


    # ophalen secties
    course_sections = canvas_course.get_sections()
    for course_section in course_sections:
        new_section = Section(course_section.id, course_section.name, "role")
        course_config.sections.append(new_section)
        if start.projects_groep_name == "SECTIONS":
            new_student_group = StudentGroup(new_section.id, new_section.name)
            course_config.student_groups.append(new_student_group)
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
        course_config.assignment_groups.append(assignment_group)

    # retrieve Teachers
    users = canvas_course.get_users(enrollment_type=['teacher', 'ta'])
    teacher_count = 0
    for user in users:
        teacher_count += 1
        # werkt helaas niet om de secties op te halen, wordt vervolgd ...
        # print("GC06 -", user["enrollments"])
        teacher = Teacher(user.id, user.name)
        course_config.teachers.append(teacher)
        print("GC07", teacher)

    canvas_group_categories = canvas_course.get_group_categories()
    for canvas_group_category in canvas_group_categories:
        print(canvas_group_category)
        # retrieve project_groups
        if canvas_group_category.name == start.projects_groep_name:
            canvas_groups = canvas_group_category.get_groups()
            for canvas_group in canvas_groups:
                studentGroup = StudentGroup(canvas_group.id, canvas_group.name)
                course_config.student_groups.append(studentGroup)
                print(canvas_group)
        # ophalen slb-groepen
        if canvas_group_category.name == start.slb_groep_name:
            canvas_groups = canvas_group_category.get_groups()
            for canvas_group in canvas_groups:
                studentGroup = StudentGroup(canvas_group.id, canvas_group.name)
                course_config.slb_groups.append(studentGroup)
                print(canvas_group)

    course_config.level_moments = start.level_moments
    course_config.attendance = start.attendance
    course_config.perspectives = start.perspectives
    course_config.roles = start.roles
    print("GC98 - ConfigFileName:", CourseInstances.get_config_file_name(instances.current_instance))
    with open(CourseInstances.get_config_file_name(instances.current_instance), 'w') as f:
        dict_result = course_config.to_json([])
        json.dump(dict_result, f, indent=2)

    print("GC99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
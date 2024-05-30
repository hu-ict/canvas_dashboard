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
    course_config = CourseConfig(canvas_course.name, (start.end_date - start.start_date).days, 0)


    # ophalen secties
    course_sections = canvas_course.get_sections()
    for course_section in course_sections:
        new_section = Section(course_section.id, course_section.name, "role")
        course_config.sections.append(new_section)
        if start.projects_groep_name == "SECTIONS":
            new_student_group = StudentGroup(new_section.id, new_section.name)
            course_config.student_groups.append(new_student_group)
        print("course_section", new_section)


    # ophalen assignments_groups and score
    canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides'])
    for canvas_assignment_group in canvas_assignment_groups:
        group_points_possible = 0
        assignment_group = AssignmentGroup(canvas_assignment_group.id, canvas_assignment_group.name, [], [], "LINEAIR",
                                           0, 0, 0, 0, 0, None)
        for canvas_assignment in canvas_assignment_group.assignments:
            if canvas_assignment['overrides']:
                for overrides in canvas_assignment['overrides']:
                    if canvas_assignment['points_possible']:
                        group_points_possible += canvas_assignment['points_possible']
                        points_possible = canvas_assignment['points_possible']
                    else:
                        points_possible = 0
                    if overrides['lock_at']:
                        assignment_date = get_date_time_obj(overrides['lock_at'])
                    else:
                        if overrides['due_at']:
                            assignment_date = get_date_time_obj(overrides['due_at'])
                        else:
                            assignment_date = start.end_date
                    if overrides['unlock_at']:
                        unlock_date = get_date_time_obj(overrides['unlock_at'])
                    else:
                        unlock_date = start.start_date

                    if 'course_section_id' in overrides.keys():
                        section_id = overrides['course_section_id']
                    else:
                        section_id = 0
                    # assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'],
                    #                         canvas_assignment['assignment_group_id'], section_id,
                    #                         canvas_assignment['grading_type'],
                    #                         canvas_assignment['grading_standard_id'],
                    #                         points_possible, assignment_date, unlock_date, date_to_day(start.start_date, assignment_date))
                    # assignment_group.append_assignment(assignment)
            else:
                if canvas_assignment['points_possible']:
                    group_points_possible += canvas_assignment['points_possible']
                    points_possible = canvas_assignment['points_possible']
                else:
                    points_possible = 0

                if canvas_assignment['unlock_at']:
                    unlock_date = canvas_assignment['unlock_at']
                else:
                    unlock_date = start.start_date
                if canvas_assignment['lock_at']:
                    assignment_date = get_date_time_obj(canvas_assignment['lock_at'])
                else:
                    if canvas_assignment['due_at']:
                        assignment_date = get_date_time_obj(canvas_assignment['due_at'])
                    else:
                        assignment_date = start.end_date
                if canvas_assignment['unlock_at']:
                    unlock_date = get_date_time_obj(canvas_assignment['unlock_at'])
                else:
                    unlock_date = start.start_date
                assignment = Assignment(canvas_assignment['id'],
                                        canvas_assignment['name'],
                                        canvas_assignment['assignment_group_id'],
                                        0,
                                        canvas_assignment['grading_type'],
                                        canvas_assignment['grading_standard_id'],
                                        points_possible,
                                        assignment_date,
                                        unlock_date,
                                        date_to_day(start.start_date, assignment_date))
                # assignment_group.append_assignment(assignment)
        assignment_group.total_points = group_points_possible
        print("assignment_group_2", canvas_assignment_group, "points", group_points_possible, assignment_group.strategy)
        course_config.assignment_groups.append(assignment_group)

    # ophalen Teachers
    users = canvas_course.get_users(enrollment_type=['teacher', 'ta'])
    teacher_count = 0
    for user in users:
        teacher_count += 1
        teacher = Teacher(user.id, user.name)
        course_config.teachers.append(teacher)
        print(teacher)

    canvas_group_categories = canvas_course.get_group_categories()
    for canvas_group_category in canvas_group_categories:
        print(canvas_group_category)
        # ophalen secties projectgroepen
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

    course_config.progress = start.progress
    course_config.perspectives = start.perspectives
    course_config.roles = start.roles
    with open(start.config_file_name, 'w') as f:
        dict_result = course_config.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)

    print("Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
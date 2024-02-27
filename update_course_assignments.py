import json
import sys

from canvasapi import Canvas
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import API_URL, get_date_time_obj, get_actual_date, date_to_day
from lib.file import read_start, read_course, read_course_instance
from model.Assignment import Assignment


def get_dates(input, start):
    if input['due_at']:
        assignment_date = get_date_time_obj(input['due_at'])
    else:
        if input['lock_at']:
            assignment_date = get_date_time_obj(input['lock_at'])
        else:
            assignment_date = start.end_date
    if input['unlock_at']:
        unlock_date = get_date_time_obj(input['unlock_at'])
    else:
        unlock_date = start.start_date
    return unlock_date, assignment_date

def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())

    course = read_course(start.course_file_name)
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print(user.name)
    canvas_course = canvas.get_course(start.canvas_course_id)

    # Update Assignments bij de AssignmentsGroups
    canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides', 'online_quiz'])
    for canvas_assignment_group in canvas_assignment_groups:
        # use only relevant assignment_groups
        assignment_group = course.find_assignment_group(canvas_assignment_group.id)
        if assignment_group:
            print("assignment_group", canvas_assignment_group)
            group_points_possible = 0
            for canvas_assignment in canvas_assignment_group.assignments:
                if canvas_assignment['points_possible']:
                    group_points_possible += canvas_assignment['points_possible']
                    points_possible = canvas_assignment['points_possible']
                else:
                    points_possible = 0

                # l_submission_types = canvas_assignment['submission_types']
                # print(l_submission_types)
                # if 'external_tool' in l_submission_types:
                #     print(canvas_assignment['quiz_id'])
                if canvas_assignment['overrides']:
                    for overrides in canvas_assignment['overrides']:
                        unlock_date, assignment_date = get_dates(overrides, start)
                        if 'course_section_id' in overrides.keys():
                            section_id = overrides['course_section_id']
                        else:
                            section_id = 0
                        assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'], canvas_assignment['assignment_group_id'], section_id, points_possible, assignment_date, unlock_date, date_to_day(start.start_date, assignment_date))
                        print("OVERRIDE", assignment)
                        assignment_group.append_assignment(assignment)
                else:
                    unlock_date, assignment_date = get_dates(canvas_assignment, start)
                    section_id = 0
                    assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'],
                                        canvas_assignment['assignment_group_id'], section_id,
                                        points_possible, assignment_date, unlock_date, date_to_day(start.start_date, assignment_date))

                    print(assignment)
                    assignment_group.append_assignment(assignment)
            print(assignment_group.name, assignment_group.total_points, group_points_possible)
            # assignment_group.total_points = group_points_possible

    with open(start.course_file_name, 'w') as f:
        dict_result = course.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)

    print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

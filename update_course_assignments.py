import json
from canvasapi import Canvas
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import API_URL, actual_date, DATE_TIME_STR, get_date_time_obj
from lib.file import read_start, read_config, read_course
from model.Assignment import Assignment
from model.Perspective import Perspective
from model.Student import Student


def get_dates(input):
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

start = read_start()
course = read_course(start.course_file_name)
# Initialize a new Canvas object
canvas = Canvas(API_URL, start.api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course = canvas.get_course(start.course_id)

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
                    unlock_date, assignment_date = get_dates(overrides)
                    if 'course_section_id' in overrides.keys():
                        section_id = overrides['course_section_id']
                    else:
                        section_id = 0
                    assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'], canvas_assignment['assignment_group_id'], section_id, points_possible, assignment_date, unlock_date)
                    print("OVERRIDE", assignment)
                    assignment_group.append_assignment(assignment)
            else:
                unlock_date, assignment_date = get_dates(canvas_assignment)
                section_id = 0
                assignment = Assignment(canvas_assignment['id'], canvas_assignment['name'],
                                    canvas_assignment['assignment_group_id'], section_id,
                                    points_possible, assignment_date, unlock_date)
                print(assignment)
                assignment_group.append_assignment(assignment)
        print(assignment_group.name, assignment_group.total_points, group_points_possible)
        # assignment_group.total_points = group_points_possible

with open(start.course_file_name, 'w') as f:
    dict_result = course.to_json(["assignment"])
    json.dump(dict_result, f, indent=2)

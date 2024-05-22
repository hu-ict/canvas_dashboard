import json
import sys

from canvasapi import Canvas
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import API_URL, get_date_time_obj, date_to_day, get_actual_date
from lib.file import read_start, read_config, read_course_instance
from model.Assignment import Assignment
from model.Criterion import Criterion
from model.Rating import Rating


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


def get_uses_assignment_groups(config):
    uses_assignment_groups = []
    if len(config.progress.assignment_groups) > 0:
        uses_assignment_groups += config.progress.assignment_groups
    else:
        print("P01 - WARNING no assignments_group for progress perspective ", config.progress.name)

    for perspective in config.perspectives.values():
        if len(perspective.assignment_groups) > 0:
            uses_assignment_groups += perspective.assignment_groups
        else:
            print("P02 - WARNING no assignments_group for perspective ", perspective.name)

    print("P03 - Used assignment_groups", uses_assignment_groups)
    return uses_assignment_groups


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
    uses_assignment_groups = get_uses_assignment_groups(config)
    canvas_course = canvas.get_course(start.canvas_course_id)
    # Ophalen Assignments bij de AssignmentsGroups
    canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides', 'online_quiz'])
    for canvas_assignment_group in canvas_assignment_groups:
        # use only relevant assignment_groups
        assignment_group = config.find_assignment_group(canvas_assignment_group.id)
        # print("C61 -", "assignment_group", canvas_assignment_group.id)
        if assignment_group and assignment_group.id in uses_assignment_groups:
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
                        print("C75 - WARNING inconsistency in ", assignment.name, "assignment points", assignment.points, "rubrics points", rubrics_points)
                    else:
                        assignment.points = rubrics_points
                        # print("C76 -", assignment.name, "points", assignment.points, "criteria aantal", len(assignment.rubrics))
                    total_rubrics_points += rubrics_points
                except:
                    print("C77 - WARNING No rubric", canvas_assignment.name)
                if assignment_group.strategy == "POINTS":
                    assignment_group.total_points = total_group_points
                else:
                    assignment_group.total_points = total_rubrics_points
            print("C78 -", assignment_group.name, "total_group_points", total_group_points, "total_rubrics_points", total_rubrics_points)
            # assignment_group.total_points = group_points_possible
        else:
            print(f"C79 - assignment_group {canvas_assignment_group.name} is not used")

    for assignment_group in config.assignment_groups:
        assignment_group.assignments = sorted(assignment_group.assignments, key=lambda a: a.assignment_day)
        if assignment_group.strategy == "NONE":
            assignment_group.bandwidth = None
        else:
            assignment_group.bandwidth = bandwidth_builder(assignment_group, config.days_in_semester)

    with open(start.course_file_name, 'w') as f:
        dict_result = config.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)

    print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("generate_course.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
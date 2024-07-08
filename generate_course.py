import json
import sys

from canvasapi import Canvas
from lib.lib_bandwidth import bandwidth_builder, bandwidth_builder_attendance
from lib.lib_date import API_URL, get_date_time_obj, date_to_day, get_actual_date
from lib.file import read_start, read_config, read_course_instance
from model.Assignment import Assignment
from model.Criterion import Criterion
from model.Rating import Rating
from model.perspective.AttendanceMoment import AttendanceMoment

def get_tag(name):
    pos = name.find("#") + 1
    str = name[pos:].strip()
    if str[-1] == ")":
        str = str[:-1]
    return str


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
        # print("GC71 -", criterion)
        rubrics_points += criterion.points
        rubrics.append(criterion)
        for canvas_rating in canvas_criterium['ratings']:
            criterion.ratings.append(Rating(canvas_rating['id'], canvas_rating['points'], canvas_rating['description']))
    return rubrics, rubrics_points


def get_uses_assignment_groups(config):
    uses_assignment_groups = []
    if config.level_moments is not None:
        if len(config.level_moments.assignment_groups) > 0:
            uses_assignment_groups += config.level_moments.assignment_groups
        else:
            print("GC01 - WARNING no assignments_group for level_moments perspective ", config.level_moments.name)
    else:
        print("GC03 - NO level_moments perspective ")

    for perspective in config.perspectives.values():
        if len(perspective.assignment_groups) > 0:
            uses_assignment_groups += perspective.assignment_groups
        else:
            print("GC05 - WARNING no assignments_group for perspective ", perspective.name)

    print("GC07 - Used assignment_groups", uses_assignment_groups)
    return uses_assignment_groups


def get_attendance(attendance):
    starting_days = attendance.policy.starting_days
    if len(starting_days) == 0:
        print("GC81 - ERROR - Geen starting_days opgegeven in attendance.policy")
        return None
    if "WEEKLY" not in attendance.policy.recurring:
        print(f"GC81 - ERROR - Ongeldige recurring [{attendance.policy.recurring}] opgegeven in attendance.policy")
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


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GC02 -", "Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    config = read_config(instances.get_config_file_name(instances.current_instance))
    if config.attendance is not None:
        attendance = get_attendance(config.attendance)
        if attendance is not None:
            config.attendance = attendance
    # for teacher in config.teachers:
    #     print("GC04 -", teacher)
    # print("GC02 -", "Config", config)
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GC03 -", user.name)
    uses_assignment_groups = get_uses_assignment_groups(config)
    canvas_course = canvas.get_course(start.canvas_course_id)
    # Ophalen Assignments bij de AssignmentsGroups
    canvas_assignment_groups = canvas_course.get_assignment_groups(include=['assignments', 'overrides', 'online_quiz'])
    for canvas_assignment_group in canvas_assignment_groups:
        # use only relevant assignment_groups
        assignment_group = config.find_assignment_group(canvas_assignment_group.id)
        # print("GC21 -", "assignment_group", canvas_assignment_group.id)

        if assignment_group and assignment_group.id in uses_assignment_groups:
            tags = []
            print(f"GC22 - assignment_group {assignment_group.name} is used with strategy {assignment_group.strategy}")
            for c_assignment in canvas_assignment_group.assignments:
                canvas_assignment = canvas_course.get_assignment(c_assignment['id'], include=['overrides', 'online_quiz'])
                print("GC23 -", canvas_assignment.name, "grading_type:", canvas_assignment.grading_type, "grading_standard_id:", canvas_assignment.grading_standard_id)
                points_possible = 0
                if canvas_assignment.grading_type == "points":
                    if canvas_assignment.points_possible:
                        points_possible = canvas_assignment.points_possible
                    else:
                        print(f"GC64 - WARNING [{canvas_assignment.grading_type}] points_possible is not set for", canvas_assignment.name)
                elif canvas_assignment.grading_type == "pass_fail":
                    if canvas_assignment.points_possible == 0:
                        points_possible = 2
                    else:
                        points_possible = canvas_assignment.points_possible
                elif canvas_assignment.grading_type == 'letter_grade':
                    if canvas_assignment.points_possible:
                        points_possible = canvas_assignment.points_possible
                    else:
                        print(f"GC65 - WARNING [{canvas_assignment.grading_type}] points_possible is not set for", canvas_assignment.name)
                else:
                    print(f"GC26 - ERROR - {canvas_assignment.grading_type} AFGEWEZEN grading_type {canvas_assignment.name} points_possible {canvas_assignment.points_possible}")
                    continue
                if canvas_assignment.overrides:
                    for overrides in canvas_assignment.overrides:
                        unlock_date, assignment_date = get_dates(start, overrides)
                        if hasattr(overrides, "course_section_id"):
                            section_id = overrides.course_section_id
                        else:
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
                if assignment.grading_type == "pass_fail" or assignment.grading_type == "letter_grade":
                    if hasattr(canvas_assignment, "rubric"):
                        assignment.rubrics, rubrics_points = get_rubrics(canvas_assignment.rubric)
                        assignment.points = rubrics_points
                        # print("GC31 - ",len(assignment.rubrics))
                        if assignment.points > 0 and assignment.points != rubrics_points:
                            print("GC33 - WARNING inconsistency in", assignment.name, "assignment points", assignment.points, "rubrics points", rubrics_points)
                    else:
                        print("GC34 - INFO No rubric", assignment.name, "grading_type", assignment.grading_type)

                elif assignment.grading_type == "points":
                    if hasattr(canvas_assignment, "rubric"):
                        assignment.rubrics, rubrics_points = get_rubrics(canvas_assignment.rubric)
                        if assignment.points > 0 and assignment.points != rubrics_points:
                            print("GC36 - WARNING inconsistency in", assignment.name, "assignment points", assignment.points, "rubrics points", rubrics_points)
                    else:
                        print("GC38 - WARNING No rubric", assignment.name, "grading_type", assignment.grading_type)
                else:
                    print("GC40 - ERROR Unsupported grading_type", assignment.grading_type)
            total_group_points = 0
            for assignment in assignment_group.assignments:
                if "#" in assignment.name:
                    tag = get_tag(assignment.name)
                    if tag in tags:
                        pass
                    else:
                        total_group_points += assignment.points
                        tags.append(tag)
                else:
                    total_group_points += assignment.points
            assignment_group.total_points = total_group_points
            print("GC47 -", tags)
            print("GC51 -", assignment_group.name, "punten:", assignment_group.total_points)
        else:
            print(f"GC41 - assignment_group {canvas_assignment_group.name} is not used")

    for assignment_group in config.assignment_groups:
        assignment_group.assignments = sorted(assignment_group.assignments, key=lambda a: a.assignment_day)
        if assignment_group.strategy == "NONE":
            assignment_group.bandwidth = None
        elif assignment_group.total_points == 0:
            print("GC81 - ERROR Couldn't calculate bandwidth for assignment_group", assignment_group.name, "total_points is zero")
        else:
            assignment_group.bandwidth = bandwidth_builder(assignment_group, config.days_in_semester)
    if config.attendance is not None:
        config.attendance.bandwidth = bandwidth_builder_attendance(config.attendance.lower_points, config.attendance.upper_points, config.attendance.total_points, config.days_in_semester)

    with open(instances.get_course_file_name(instances.current_instance), 'w') as f:
        dict_result = config.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)

    print("GC99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GC01 generate_course.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
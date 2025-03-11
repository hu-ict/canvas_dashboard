import json
import sys

from canvasapi import Canvas
from lib.lib_bandwidth import bandwidth_builder, bandwidth_builder_attendance
from lib.lib_date import API_URL, get_date_time_obj, date_to_day, get_actual_date
from lib.file import read_start, read_course_instances, read_config_from_canvas
from model.Assignment import Assignment
from model.Criterion import Criterion
from model.Rating import Rating
from model.perspective.AttendanceMoment import AttendanceMoment


def get_tags(name):
    pos = name.find("(") + 1
    str = name[pos:].strip()
    if str[-1] == ")":
        str = str[:-1]
    tags = str.split()
    return tags


def get_dates(config, input):
    if input.due_at:
        assignment_date = get_date_time_obj(input.due_at)
    else:
        if input.lock_at:
            assignment_date = get_date_time_obj(input.lock_at)
        else:
            assignment_date = config.end_date
    if input.unlock_at:
        unlock_date = get_date_time_obj(input.unlock_at)
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
        if len(config.level_moments.assignment_groups) > 0:
            used_assignment_groups += config.level_moments.assignment_groups
        else:
            message = "GC01 - WARNING no assignments_group for level_moments perspective ", config.level_moments.name
            print(message)
    else:
        print("GC03 - NO level_moments perspective ")

    if config.grade_moments is not None:
        if len(config.grade_moments.assignment_groups) > 0:
            used_assignment_groups += config.grade_moments.assignment_groups
        else:
            message = "GC05 - WARNING no assignments_group for grade_moments perspective ", config.grade_moments.name
            print(message)
    else:
        print("GC07 - NO level_moments perspective ")

    for perspective in config.perspectives.values():
        if len(perspective.assignment_groups) > 0:
            used_assignment_groups += perspective.assignment_groups
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


def generate_course(instance_name):
    print("GCS01 - generate_course.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("GCS02 -", "Instance:", instance.name)
    start = read_start(instance.get_start_file_name())
    canvas = Canvas(API_URL, start.api_key)
    canvas_course = canvas.get_course(start.canvas_course_id)
    config = read_config_from_canvas(canvas_course)
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
        assignment_group = config.find_assignment_group(canvas_assignment_group.id)
        # print("GC21 -", "assignment_group", canvas_assignment_group.id)

        if assignment_group and assignment_group.id in uses_assignment_groups:
            tags = []
            role = config.get_role_by_assignment_groep(assignment_group.id)
            if role is not None:
                assignment_group.role = role.name
            else:
                assignment_group.role = "Iedereen"

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
                        message = f"GCS64 - WARNING [{canvas_assignment.grading_type}] points_possible is not set for", canvas_assignment.name
                        print(message)
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
                tags_lu = []
                if "#" in assignment.name or "@" in assignment.name:
                    tags = get_tags(assignment.name)
                    for t in tags:
                        # print("GC60 -", t)
                        if "#" in t[0]:
                            if "LU" in t:
                                tags_lu.append(t[1:])
                            else:
                                tag_sequence = t[1:]
                            break
                    for t in tags:
                        if "@" in t[0]:
                            tags_lu.append(t[1:])
                for tag_lu in tags_lu:
                    # print("GC61 - LU", tag_lu)
                    learning_outcome = config.find_learning_outcome(tag_lu)
                    # print("GC62 - LU", learning_outcome)
                    if learning_outcome is not None:
                        assignment.learning_outcomes.append(learning_outcome.id)

                if assignment.grading_type == "pass_fail":
                    if hasattr(canvas_assignment, "rubric"):
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
    # collect all LU from Assignment and copy them AssignmentSequence
    for assignment_group in config.assignment_groups:
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                for learning_outcome_id in assignment.learning_outcomes:
                    #establish many-2-many relation
                    learning_outcome = config.find_learning_outcome(learning_outcome_id)
                    assignment_sequence.add_learning_outcome(learning_outcome_id)
                    learning_outcome.add_assigment_sequence(assignment_sequence.tag)
                assignment.name = assignment.name.split("(")[0].strip()
            assignment_sequence.name = assignment_sequence.name.split("(")[0].strip()
    for assignment_group in config.assignment_groups:
        assignment_group.assignment_sequences = sorted(assignment_group.assignment_sequences, key=lambda a: a.get_day())
        assignment_group.bandwidth = bandwidth_builder(assignment_group, config.days_in_semester)
    if config.attendance is not None:
        config.attendance.bandwidth = bandwidth_builder_attendance(config.attendance.lower_points, config.attendance.upper_points, config.attendance.total_points, config.days_in_semester)

    with open(instance.get_course_file_name(), 'w') as f:
        dict_result = config.to_json()
        json.dump(dict_result, f, indent=2)

    print("GCS99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_course(sys.argv[1])
    else:
        generate_course("")

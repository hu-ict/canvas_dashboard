import logging
from typing import List, Tuple
import json
import sys


# Placeholder imports for original functionality
from canvasapi import Canvas
from lib.lib_date import API_URL, get_date_time_obj, get_actual_date
from lib.file import read_environment, read_secret_api_key, read_dashboard_from_canvas, read_config_from_canvas, read_course
from model.rubric.Criterion import Criterion
from model.rubric.Rating import Rating
from model.attendance.AttendanceMoment import AttendanceMoment

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
GRADING_TYPES = {"POINTS": "points", "PASS_FAIL": "pass_fail", "LETTER": "letter_grade"}
DEFAULT_POINTS = 2


def get_tags(name: str) -> List[str]:
    """Extract tags from assignment name."""
    pos = name.find("(") + 1
    tag_str = name[pos:].strip()
    if tag_str.endswith(")"):
        tag_str = tag_str[:-1]
    return tag_str.split()


def get_dates(config, canvas_object) -> Tuple[str, str]:
    """Return unlock and assignment dates based on Canvas object."""
    assignment_date = (
        get_date_time_obj(canvas_object.due_at)
        if canvas_object.due_at
        else get_date_time_obj(canvas_object.lock_at) if canvas_object.lock_at else config.end_date
    )
    unlock_date = (
        get_date_time_obj(canvas_object.unlock_at)
        if canvas_object.unlock_at
        else config.start_date
    )
    return unlock_date, assignment_date


def get_rubrics(canvas_rubrics) -> Tuple[list, int]:
    """Extract rubrics and calculate total points."""
    rubrics_points = 0
    rubrics = []
    for canvas_criterium in canvas_rubrics:
        criterion = Criterion(canvas_criterium['id'], canvas_criterium['points'], canvas_criterium['description'])
        rubrics_points += criterion.points
        rubrics.append(criterion)
        for canvas_rating in canvas_criterium['ratings']:
            criterion.ratings.append(Rating(canvas_rating['id'], canvas_rating['points'], canvas_rating['description']))
    return rubrics, rubrics_points


def calculate_points(canvas_assignment, rubrics_points: int) -> int:
    """Calculate points based on grading type and rubrics."""
    if canvas_assignment.grading_type in [GRADING_TYPES["POINTS"], GRADING_TYPES["PASS_FAIL"], GRADING_TYPES["LETTER"]]:
        return rubrics_points if rubrics_points > 0 else canvas_assignment.points_possible or DEFAULT_POINTS
    raise ValueError(f"Unsupported grading type: {canvas_assignment.grading_type}")


def get_used_assignment_groups(config) -> List[int]:
    """Collect all used assignment group IDs from config."""
    used_assignment_groups = []
    for perspective in [config.level_moments, config.grade_moments] + list(config.perspectives.values()):
        if perspective and len(perspective.assignment_group_ids) > 0:
            used_assignment_groups += perspective.assignment_group_ids
        else:
            logging.warning(f"No assignments_group for perspective {getattr(perspective, 'name', 'unknown')}")
    logging.info(f"Used assignment_groups: {used_assignment_groups}")
    return used_assignment_groups


def get_attendance(attendance):
    """Generate attendance moments based on policy."""
    starting_days = attendance.policy.starting_days
    if not starting_days:
        logging.error("Geen starting_days opgegeven in attendance.policy")
        return None
    if "WEEKLY" not in attendance.policy.recurring:
        logging.error(f"Ongeldige recurring [{attendance.policy.recurring}] opgegeven in attendance.policy")
        return None
    for week in range(attendance.policy.times):
        if week + 1 in attendance.policy.exceptions:
            continue
        day = starting_days[0] + week * 7
        attendance.attendance_moments.append(AttendanceMoment(day, DEFAULT_POINTS))
    return attendance


def generate_course(course_code: str, instance_name: str) -> None:
    """Main function to generate course configuration."""
    logging.info("Start generate_course")
    g_actual_date = get_actual_date()

    try:
        environment = read_environment(ENVIRONMENT_FILE_NAME)
        secret_api_key = read_secret_api_key(SECRET_API_KEY_FILE_NAME)
    except Exception as e:
        logging.error(f"Failed to read environment or API key: {e}")
        return

    if instance_name:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        try:
            with open(ENVIRONMENT_FILE_NAME, 'w') as f:
                json.dump(environment.to_json(), f, indent=2)
        except IOError as e:
            logging.error(f"Failed to write environment file: {e}")
            return

    course_instance = environment.get_instance_of_course(environment.current_instance)
    logging.info(f"Instance: {course_instance.name}")

    canvas = Canvas(API_URL, secret_api_key.canvas_api_key)
    canvas_course = canvas.get_course(course_instance.canvas_course_id)

    dashboard = read_dashboard_from_canvas(canvas_course)
    with open(course_instance.get_dashboard_file_name(), 'w') as f:
        json.dump(dashboard.to_json(), f, indent=2)

    config = read_config_from_canvas(canvas_course) if course_instance.stage == "PROD" else read_course(
        course_instance.get_config_file_name())
    user = canvas.get_current_user()
    logging.info(f"Current user: {user.name}")

    if config.attendance:
        attendance = get_attendance(config.attendance)
        if attendance:
            config.attendance = attendance

    used_groups = get_used_assignment_groups(config)

    logging.info(f"Time running: {(get_actual_date() - g_actual_date).seconds} seconds")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        generate_course(sys.argv[1], sys.argv[2])
    else:
        generate_course('', '')

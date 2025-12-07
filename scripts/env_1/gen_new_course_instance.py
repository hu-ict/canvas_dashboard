
#!/usr/bin/env python3
"""
Generate a new course instance and update the environment configuration.

Original dependencies:
- lib.file.read_environment
- model.environment.CourseInstance
- model.environment.Environment (ENVIRONMENT_FILE_NAME)
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path
from typing import Dict

from scripts.lib.file import read_environment
from model.environment.CourseInstance import CourseInstance
from model.environment.Environment import ENVIRONMENT_FILE_NAME

# --------------------------------
# Logging
# --------------------------------
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# --------------------------------
# Constants (education periods)
# --------------------------------
PERIODS: Dict[str, Dict[str, str]] = {
    "sep25": {"start_date": "2025-09-01T00:00:00Z", "end_date": "2026-01-30T23:59:59Z"},
    "feb26": {"start_date": "2026-02-09T00:00:00Z", "end_date": "2026-07-10T23:59:59Z"},
    "sep26": {"start_date": "2026-08-31T00:00:00Z", "end_date": "2027-01-29T23:59:59Z"},
}

# --------------------------------
# Helpers
# --------------------------------
def _write_json_file(path: Path, data: dict) -> None:
    """Write a Python dict as JSON to a file."""
    try:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.debug("Written JSON to %s", path)
    except Exception as exc:
        logger.error("Failed to write %s: %s", path, exc)
        raise


def _validate_course_code(course_code: str) -> None:
    """
    Validate course_code:
    - Not empty
    - 2-20 characters
    - Only letters, digits, underscore, or hyphen
    """
    if not course_code:
        raise ValueError("Course code cannot be empty.")
    if not (2 <= len(course_code) <= 20):
        raise ValueError("Course code must be between 2 and 20 characters.")
    if not re.match(r"^[A-Za-z0-9_-]+$", course_code):
        raise ValueError("Course code may only contain letters, digits, underscores, or hyphens.")


def _validate_instance_name(instance_name: str) -> None:
    """
    Validate course_instance_name:
    - Not empty
    - 2-40 characters
    - Allowed chars: letters, digits, space, underscore, hyphen
    """
    if not instance_name:
        raise ValueError("Course instance name cannot be empty.")
    if not (2 <= len(instance_name) <= 40):
        raise ValueError("Course instance name must be between 2 and 40 characters.")
    if not re.match(r"^[A-Za-z0-9 _-]+$", instance_name):
        raise ValueError("Course instance name may only contain letters, digits, spaces, underscores, or hyphens.")


def _validate_canvas_course_id(canvas_course_id: str) -> None:
    """
    Validate Canvas course id:
    - Not empty
    - Digits only (adjust if your IDs can be alphanumeric)
    """
    if not canvas_course_id:
        raise ValueError("Canvas course id cannot be empty.")
    if not re.match(r"^[0-9]+$", canvas_course_id):
        raise ValueError("Canvas course id must contain only digits.")


def _validate_target_path(target_path: str) -> None:
    """
    Validate target path:
    - Not empty
    - Basic sanity check on length and characters
    (We do not check existence here because it can be a OneDrive path or to-be-created path.)
    """
    if not target_path:
        raise ValueError("Target path cannot be empty.")
    if len(target_path) < 3:
        raise ValueError("Target path seems too short.")
    # Allow common path characters; reject control chars
    if re.search(r"[\x00-\x1F]", target_path):
        raise ValueError("Target path contains invalid control characters.")


def _validate_period(period: str) -> None:
    if period not in PERIODS:
        raise ValueError(f"Period '{period}' is not one of {list(PERIODS.keys())}.")


def _ensure_instance_is_unique(environment, course_code: str, instance_name: str) -> None:
    course = environment.get_course_by_name(course_code)
    if course.get_course_instance_by_name(instance_name) is not None:
        raise ValueError(f"Course instance '{instance_name}' already exists for course '{course_code}'.")


def _ensure_directories(course_instance) -> None:
    """
    Create required directories for the course instance (if not present).
    """
    for path_getter in (
        course_instance.get_project_path,
        course_instance.get_temp_path,
        course_instance.get_html_index_path,
        course_instance.get_html_general_path,
        course_instance.get_html_student_path,
    ):
        p = Path(path_getter())
        p.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------
# Core
# --------------------------------
def create_course_instance(
    course_code: str,
    instance_name: str,
    canvas_course_id: str,
    target_path: str,
    period: str,
    environment_file: str = ENVIRONMENT_FILE_NAME,
    stage: str = "DEV",
    attendance_file: str | None = None,  # kept for future extension
) -> None:
    """
    Create a new CourseInstance for an existing course and update the environment.
    """
    # Validate inputs
    _validate_course_code(course_code)
    _validate_instance_name(instance_name)
    _validate_canvas_course_id(canvas_course_id)
    _validate_target_path(target_path)
    _validate_period(period)

    logger.info("Creating course instance '%s' for course '%s'", instance_name, course_code)

    environment = read_environment(environment_file)

    # Ensure course exists
    if course_code not in environment.get_course_names():
        raise ValueError(f"Course code '{course_code}' does not exist in environment.")

    # Ensure instance is unique
    _ensure_instance_is_unique(environment, course_code, instance_name)

    # Build instance
    course = environment.get_course_by_name(course_code)
    course_instance = CourseInstance(
        instance_name,
        course_code,
        canvas_course_id,
        target_path,
        PERIODS[period],
        stage,
    )

    # Add to environment
    course.course_instances.append(course_instance)

    # Create directories
    _ensure_directories(course_instance)

    # Update current instance pointer
    environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}

    # Persist environment
    _write_json_file(Path(environment_file), environment.to_json())

    # Optional: future use of attendance_file (not used in original script)
    if attendance_file:
        logger.info("Attendance file provided: %s (currently not persisted by this script)", attendance_file)

    logger.info("CourseInstance created: %s", instance_name)
    logger.info("Environment updated: %s", environment.name)


# --------------------------------
# CLI
# --------------------------------
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a new course instance and update the environment configuration."
    )
    parser.add_argument("course_code", help="Existing course code (e.g., INF1A).")
    parser.add_argument("instance_name", help="Name for the new course instance (e.g., 2025-P2).")
    parser.add_argument("canvas_course_id", help="Canvas course id (digits).")
    parser.add_argument("target_path", help="Target path (e.g., OneDrive folder path).")
    parser.add_argument(
        "period",
        choices=list(PERIODS.keys()),
        help=f"Education period key: {', '.join(PERIODS.keys())}",
    )
    parser.add_argument("--stage", default="DEV", help="Stage label for the instance (default: DEV).")
    parser.add_argument("--attendance-file", default=None, help="Optional path to attendance_report.csv.")
    parser.add_argument("--env-file", default=ENVIRONMENT_FILE_NAME, help="Environment file path.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        create_course_instance(
            course_code=args.course_code,
            instance_name=args.instance_name,
            canvas_course_id=args.canvas_course_id,
            target_path=args.target_path,
            period=args.period,
            environment_file=args.env_file,
            stage=args.stage,
            attendance_file=args.attendance_file,
        )
    except ValueError as ve:
        logger.error("Invalid input: %s", ve)
        raise SystemExit(1)
    except Exception as exc:
        logger.exception("Error creating course instance: %s", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Generate a new course and update the environment configuration.

"""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path

from scripts.lib.file import read_environment
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME
from scripts.model.environment.Course import Course


# ----------------------------
# Logging setup
# ----------------------------
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


# ----------------------------
# Helpers
# ----------------------------

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
    if not re.match(r"^[A-Z 0-9_-]+$", course_code):
        raise ValueError("Course code may only contain letters, digits, underscores, or hyphens.")


def create_new_course(course_code: str) -> None:
    """
    Create a new course and update the environment file.
    """
    # Validate input
    _validate_course_code(course_code)

    logger.info("Creating new course: %s", course_code)

    environment = read_environment(ENVIRONMENT_FILE_NAME)

    # Check if course already exists
    if course_code in environment.get_course_names():
        logger.warning("Course code already exists: %s", course_code)
        logger.info("Existing courses: %s", environment.get_course_names())
        return

    # Create course object
    course = Course(course_code)
    environment.courses.append(course)

    # Ensure directory exists
    course_path = Path(course.get_path())
    course_path.parent.mkdir(parents=True, exist_ok=True)

    # Write updated environment
    _write_json_file(Path(ENVIRONMENT_FILE_NAME), environment.to_json())

    logger.info("Course successfully created: %s", course_code)
    logger.info("Environment updated: %s", ENVIRONMENT_FILE_NAME)


# ----------------------------
# CLI
# ----------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a new course and update environment.")
    parser.add_argument("course_code", help="Course code for the new course (e.g., TICT-V3SE6-25).")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        create_new_course(args.course_code)
    except ValueError as ve:
        logger.error("Invalid course code: %s", ve)
        raise SystemExit(1)
    except Exception as exc:
        logger.exception("Error creating new course: %s", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
Generate user data (CSV) for a Canvas course instance.

External dependencies (as in your current project):
- lib.file: read_course, read_environment
- lib.lib_date: get_actual_date
- model.environment.Environment: ENVIRONMENT_FILE_NAME and Environment object interface

This module focuses on:
- type safety
- clean separation of concerns
- robust CLI and error handling
- structured logging instead of opaque print codes (GUD01, etc.)
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List

from scripts.lib.file import read_course, read_environment
from lib.lib_date import get_actual_date
from model.environment.Environment import ENVIRONMENT_FILE_NAME


# ----------------------------
# Configuration & Logging
# ----------------------------

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


# ----------------------------
# Data model
# ----------------------------

@dataclass(frozen=True)
class UserRow:
    canvas_course_id: str
    course_name: str
    instance_name: str
    start_date: str
    end_date: str
    user_name: str
    user_email: str
    user_role: str  # "STUDENT" | "TEACHER"

    def to_dict(self) -> dict:
        # csv.DictWriter wil een dict
        return asdict(self)


# ----------------------------
# Core logic
# ----------------------------

def _build_user_rows(course_instance, course) -> List[UserRow]:
    """Maak alle UserRow records op basis van course instance + course inhoud."""
    base_kwargs = dict(
        canvas_course_id=course_instance.canvas_course_id,
        course_name=course_instance.course_code,
        instance_name=course_instance.name,
        start_date=course_instance.period["start_date"],
        end_date=course_instance.period["end_date"],
    )

    rows: List[UserRow] = []

    # Studenten
    for student in getattr(course, "students", []):
        rows.append(
            UserRow(
                **base_kwargs,
                user_name=student.name,
                user_email=student.email,
                user_role="STUDENT",
            )
        )

    # Docenten (noem variabele enkelvoud voor duidelijkheid)
    for teacher in getattr(course, "teachers", []):
        rows.append(
            UserRow(
                **base_kwargs,
                user_name=teacher.name,
                user_email=teacher.email,
                user_role="TEACHER",
            )
        )

    return rows


def _write_environment_current_instance(environment, course_code: str, instance_name: str) -> None:
    """
    Werk de 'current_instance' in environment bij en schrijf terug naar schijf.
    """
    environment.current_instance = {
        "course_name": course_code,
        "course_instance_name": instance_name,
    }
    env_path = Path(ENVIRONMENT_FILE_NAME)
    try:
        dict_result = environment.to_json()
        env_path.write_text(json.dumps(dict_result, indent=2), encoding="utf-8")
        logger.debug("Environment written to %s", env_path)
    except Exception as exc:
        logger.error("Kon environment niet wegschrijven naar %s: %s", env_path, exc)
        raise


def _write_csv(user_rows: Iterable[UserRow], output_path: Path) -> None:
    """Schrijf UserRow records naar CSV."""
    fieldnames = [
        "canvas_course_id",
        "course_name",
        "instance_name",
        "start_date",
        "end_date",
        "user_name",
        "user_email",
        "user_role",
    ]

    try:
        # newline="" is correct voor csv op alle platforms; encoding expliciet
        with output_path.open(mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in user_rows:
                writer.writerow(row.to_dict())
    except Exception as exc:
        logger.error("Kon CSV niet schrijven naar %s: %s", output_path, exc)
        raise


def generate_user_data(course_code: str, instance_name: str) -> Path:
    """
    Genereer CSV met user data op basis van course_code + instance_name.

    Returns:
        Pad naar het gegenereerde CSV-bestand.
    """
    start = get_actual_date()
    logger.info("Start generate_user_data (course_code=%r, instance_name=%r)", course_code, instance_name)

    environment = read_environment(ENVIRONMENT_FILE_NAME)

    # Als een instance_name is meegegeven, werk environment bij (zoals jouw originele script deed)
    if instance_name:
        _write_environment_current_instance(environment, course_code, instance_name)

    # Haal de instance uit environment (vertrouwt op current_instance)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    logger.info("Instance gevonden: %s", course_instance.name)

    # Lees het course-bestand
    course = read_course(course_instance.get_course_file_name())

    # Bouw de rows
    user_rows = _build_user_rows(course_instance, course)

    # Schrijf CSV
    output_path = Path(course_instance.get_user_data_file_name())
    _write_csv(user_rows, output_path)

    elapsed = (get_actual_date() - start).total_seconds()  # correcter dan .seconds
    logger.info("CSV geschreven: %s | runtime = %.2fs", output_path, elapsed)

    return output_path


# ----------------------------
# CLI
# ----------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genereer user-data CSV voor een Canvas course instance."
    )
    parser.add_argument(
        "course_code",
        nargs="?",
        default="",
        help="Course code (bijv. INF1A). Laat leeg om environment.current_instance te gebruiken."
    )
    parser.add_argument(
        "instance_name",
        nargs="?",
        default="",
        help="Instance naam (bijv. 2025-Periode-2). Laat leeg om environment.current_instance te gebruiken."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Zet logging level op DEBUG."
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        output = generate_user_data(args.course_code, args.instance_name)
        print(output)  # maak CLI gemakkelijk te scripten
    except Exception as exc:
        logger.exception("Fout tijdens generate_user_data: %s", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

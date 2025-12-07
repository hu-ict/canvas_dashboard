
#!/usr/bin/env python3
"""
Generate a new environment configuration for Canvas integration.

Creates:
- Environment file
- Secret API key file
- Workflow file
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

from model.environment.Environment import Environment, ENVIRONMENT_FILE_NAME
from model.environment.Execution import Execution
from scripts.model.environment.SecretApiKey import SecretApiKey, SECRET_API_KEY_FILE_NAME
from model.environment.Workflow import Workflow, WORKFLOW_FILE_NAME

# ----------------------------
# Logging setup
# ----------------------------
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


# ----------------------------
# Helpers
# ----------------------------

def _write_json_file(path: Path, data: Any) -> None:
    """Write a Python object as JSON to a file."""
    try:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        logger.debug("Written JSON to %s", path)
    except Exception as exc:
        logger.error("Failed to write %s: %s", path, exc)
        raise


def create_environment(env_name: str, canvas_api_key: str) -> None:
    """
    Create environment, secret API key, and workflow files.
    """
    logger.info("Creating new environment: %s", env_name)

    # Build environment object
    environment = Environment(env_name, {"course_name": "", "course_instance_name": ""})
    environment.executions.extend([
        Execution("env_1", "", ""),
        Execution("env_2", "", ""),
        Execution("env_3", "", ""),
    ])

    # Secret API key
    secret_api_key = SecretApiKey(env_name, canvas_api_key)

    # Workflow
    workflow = Workflow(env_name)
    workflow.new_instance()

    # Write files
    _write_json_file(Path(ENVIRONMENT_FILE_NAME), environment.to_json())
    _write_json_file(Path(SECRET_API_KEY_FILE_NAME), secret_api_key.to_json())
    _write_json_file(Path(WORKFLOW_FILE_NAME), workflow.to_json())

    logger.info("Environment successfully created: %s", env_name)


# ----------------------------
# CLI
# ----------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a new Canvas environment configuration.")
    parser.add_argument("environment_name", help="Name for the new environment.")
    parser.add_argument("canvas_api_key", help="Your personal Canvas API key.")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        create_environment(args.environment_name, args.canvas_api_key)
    except Exception as exc:
        logger.exception("Error creating environment: %s", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

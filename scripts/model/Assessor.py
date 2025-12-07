
#!/usr/bin/env python3
"""
Assessor model with robust validation and (de)serialization helpers.

Original keys (kept for compatibility):
- teacher_id
- student_group_collection
- student_group_id
- assignment_group_id
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Dict
import json


@dataclass(frozen=True, slots=True)
class Assessor:
    teacher_id: int
    student_group_collection: str
    student_group_id: int
    assignment_group_id: int

    # --------- Validation ---------
    def __post_init__(self) -> None:
        # Normalize and validate
        normalized = {
            "teacher_id": self.teacher_id,
            "student_group_collection": self.student_group_collection.strip(),
            "student_group_id": self.student_group_id,
            "assignment_group_id": self.assignment_group_id,
        }

        # Enforce non-empty values
        for key, value in normalized.items():
            if not value:
                raise ValueError(f"{key} cannot be empty.")

        # Because we used frozen=True, we cannot assign directly; use object.__setattr__
        for key, value in normalized.items():
            object.__setattr__(self, key, value)

    # --------- Serialization ---------
    def to_json(self) -> Dict[str, str]:
        """Return JSON-serializable dict (compatible with original schema)."""
        return {
            "teacher_id": self.teacher_id,
            "student_group_collection": self.student_group_collection,
            "student_group_id": self.student_group_id,
            "assignment_group_id": self.assignment_group_id,
        }

    # Convenience alias
    def to_dict(self) -> Dict[str, str]:
        return self.to_json()

    # --------- Constructors ---------
    @staticmethod
    def from_dict(data_dict: Mapping[str, Any]) -> "Assessor":
        """
        Build Assessor from a mapping. Values are coerced to str and stripped.

        Raises:
            KeyError   - If a required key is missing
            ValueError - If values are empty after normalization
            TypeError  - If data_dict is not a Mapping
        """
        if not isinstance(data_dict, Mapping):
            raise TypeError("from_dict expects a Mapping[str, Any].")

        # Required keys (compatible with original implementation)
        required = (
            "teacher_id",
            "student_group_collection",
            "student_group_id",
            "assignment_group_id",
        )
        for key in required:
            if key not in data_dict:
                raise KeyError(f"Missing required key: {key}")

        return Assessor(
            teacher_id=int(data_dict["teacher_id"]),
            student_group_collection=str(data_dict["student_group_collection"]),
            student_group_id=int(data_dict["student_group_id"]),
            assignment_group_id=int(data_dict["assignment_group_id"]),
        )

    @classmethod
    def from_json_str(cls, json_str: str) -> "Assessor":
        """
        Build Assessor from a JSON string (dict-like), then delegates to from_dict.
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    # --------- Representations ---------
    def __str__(self) -> str:
        # Keep it concise, include the teacher_id as well
        return (
            f"Assessor({self.teacher_id}, "
            f"{self.student_group_collection}, "
            f"{self.student_group_id}, "
            f"{self.assignment_group_id})"
        )

    def __repr__(self) -> str:
        return (
            "Assessor("
            f"teacher_id={self.teacher_id!r}, "
            f"student_group_collection={self.student_group_collection!r}, "
            f"student_group_id={self.student_group_id!r}, "
            f"assignment_group_id={self.assignment_group_id!r})"
        )

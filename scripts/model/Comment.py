
#!/usr/bin/env python3
"""
Comment model with robust validation and (de)serialization helpers.

Original fields (kept for compatibility):
- author_id
- author_name
- date (datetime-like handled via lib.lib_date helpers)
- comment
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Dict
import json

from scripts.lib.lib_date import get_date_time_obj, get_date_time_str


@dataclass(frozen=True, slots=True)
class Comment:
    author_id: int
    author_name: str
    # date is stored as an object compatible with get_date_time_str/get_date_time_obj
    date: Any
    comment: str

    # --------- Validation & normalization ---------
    def __post_init__(self) -> None:
        # Trim strings; keep date as-is but validate presence
        normalized = {
            "author_id": self.author_id,
            "author_name": self.author_name.strip(),
            "comment": self.comment,
        }
        for key, value in normalized.items():
            if not value:
                raise ValueError(f"{key} cannot be empty.")

        if self.date is None:
            raise ValueError("date cannot be None.")

        # Because the dataclass is frozen, assign via object.__setattr__
        for key, value in normalized.items():
            object.__setattr__(self, key, value)

    # --------- Serialization ---------
    def to_dict(self) -> Dict[str, Any]:
        """
        Return a dict suitable for JSON serialization (keeps original schema).
        Uses get_date_time_str for date conversion (same behavior as original).
        """
        return {
            "author_id": self.author_id,
            "author_name": self.author_name,
            "date": get_date_time_str(self.date),
            "comment": self.comment,
        }

    # Convenience alias for compatibility with original code
    def to_json(self) -> Dict[str, Any]:
        return self.to_dict()

    # --------- Constructors ---------
    @staticmethod
    def from_dict(data_dict: Mapping[str, Any]) -> "Comment":
        """
        Build Comment from a mapping.
        Expects keys: author_id, author_name, date, comment.
        Converts date using get_date_time_obj (same as original).
        Raises:
            KeyError   - missing keys
            ValueError - validation errors on fields
            TypeError  - if data_dict is not a Mapping
        """
        if not isinstance(data_dict, Mapping):
            raise TypeError("from_dict expects a Mapping[str, Any].")

        required = ("author_id", "author_name", "date", "comment")
        for key in required:
            if key not in data_dict:
                raise KeyError(f"Missing required key: {key}")

        return Comment(
            author_id=int(data_dict["author_id"]),
            author_name=str(data_dict["author_name"]),
            date=get_date_time_obj(data_dict["date"]),
            comment=str(data_dict["comment"]),
        )

    @classmethod
    def from_json_str(cls, json_str: str) -> "Comment":
        """
        Build Comment from a JSON string (dict-like), then delegates to from_dict.
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    # --------- Representations ---------
    def __str__(self) -> str:
        # Keep compact but informative; date as string to ensure readability
        return f"Comment({self.author_id}, {self.author_name}, {get_date_time_str(self.date)}, {self.comment})"

    def __repr__(self) -> str:
        return (
            "Comment("
            f"author_id={self.author_id!r}, "
            f"author_name={self.author_name!r}, "
            f"date={get_date_time_str(self.date)!r}, "
            f"comment={self.comment!r})"
        )

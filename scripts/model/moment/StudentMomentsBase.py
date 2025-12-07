from abc import ABC, abstractmethod
from typing import List
from scripts.model.Submission import Submission


class StudentMomentsBase(ABC):
    def __init__(self, name: str, assignment_groups: List[int]):
        self.name = name
        self.assignment_groups = assignment_groups
        self.submissions: List[Submission] = []

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'assignment_groups': self.assignment_groups,
            'submissions': [s.to_json() for s in self.submissions]
        }

    def __str__(self) -> str:
        line = f'{self.__class__.__name__}({self.name}, {self.assignment_groups})\n'
        for submission in self.submissions:
            line += f" s {submission}\n"
        return line

    def put_submission(self, a_submission: Submission) -> None:
        """Update or add a submission."""
        for i, sub in enumerate(self.submissions):
            if sub.id == a_submission.id:
                self.submissions[i] = a_submission
                return
        self.submissions.append(a_submission)

    def get_submission_by_assignment(self, assignment_id: int) -> Submission:
        for submission in self.submissions:
            if submission.assignment.id == assignment_id:
                return submission
        return None

    @classmethod
    def from_dict(cls, data_dict: dict):
        new_obj = cls(data_dict['name'], data_dict['assignment_groups'])
        if 'submissions' in data_dict:
            new_obj.submissions = [Submission.from_dict(s) for s in data_dict['submissions']]
        return new_obj


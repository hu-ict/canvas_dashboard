from model.Assignment import Assignment
from model.LearningOutcome import LearningOutcome


class AssignmentSequence:
    def __init__(self, name, tag, grading_type, points):
        self.name = name
        self.tag = tag
        self.grading_type = grading_type
        self.points = points
        self.assignments = []
        self.learning_outcomes = []

    def __str__(self):
        return f'AssignmentSequence({self.name}, {self.tag}, {self.grading_type}, {self.points})'

    def get_day(self):
        if len(self.assignments) > 0:
            return self.assignments[0].assignment_day
        return 0

    def get_date(self):
        if len(self.assignments) > 0:
            return self.assignments[0].assignment_date
        return 0

    def get_passed_assignments(self, actual_day):
        passed_assignments = []
        for assignment in self.assignments:
            if assignment.assignment_day < actual_day:
                passed_assignments.append(assignment)
        return passed_assignments

    def get_last_passed_assignment(self, actual_day):
        last_passed_assignment = None
        for assignment in self.assignments:
            if assignment.assignment_day < actual_day:
                last_passed_assignment = assignment
        return last_passed_assignment

    def to_json(self):
        return {
            'name': self.name,
            'tag': self.tag,
            'grading_type': self.grading_type,
            'points': int(self.points),
            'assignments': list(map(lambda a: a.to_json(), self.assignments)),
            'learning_outcomes': self.learning_outcomes
        }

    @staticmethod
    def from_dict(data_dict):
        new = AssignmentSequence(data_dict['name'], data_dict['tag'], data_dict['grading_type'], data_dict['points'])
        if 'assignments' in data_dict.keys():
            new.assignments = list(map(lambda a: Assignment.from_dict(a), data_dict['assignments']))
        if 'learning_outcomes' in data_dict:
            new.learning_outcomes = data_dict['learning_outcomes']
        return new

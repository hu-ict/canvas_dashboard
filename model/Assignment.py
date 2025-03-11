from lib.lib_date import get_date_time_obj, get_date_time_str
from model.Criterion import Criterion


class Assignment:
    def __init__(self, assignment_id, name, group_id, course_section_id, grading_type, grading_standard_id, points,
                 submission_types, assignment_date, unlock_date, assignment_day, unlock_day):
        self.id = assignment_id
        self.name = name
        self.group_id = group_id
        self.section_id = course_section_id
        self.grading_type = grading_type
        self.grading_standard_id = grading_standard_id
        self.points = points
        self.submission_types = submission_types
        self.assignment_date = assignment_date
        self.unlock_date = unlock_date
        self.unlock_day = unlock_day
        self.assignment_day = assignment_day
        self.messages = []
        self.rubrics = []
        self.learning_outcomes = []
        self.sections = []

    def __str__(self):
        return f'Assignment({self.id}, {self.name}, {self.group_id}, {self.section_id}, {self.grading_type}, ' \
               f'{self.grading_standard_id}, {self.points}, {self.submission_types}, ' \
               f'{get_date_time_str(self.assignment_date)}, {self.assignment_day})'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'group_id': self.group_id,
            'section_id': self.section_id,
            'grading_type': self.grading_type,
            'grading_standard_id': self.grading_standard_id,
            'submission_types': self.submission_types,
            'unlock_date': get_date_time_str(self.unlock_date),
            'unlock_day': self.unlock_day,
            'assignment_date': get_date_time_str(self.assignment_date),
            'assignment_day': self.assignment_day,
            'points': int(self.points),
            'messages': self.messages,
            'rubrics': list(map(lambda r: r.to_json(), self.rubrics)),
            'learning_outcomes': self.learning_outcomes,
            'sections': self.sections
        }

    def get_criterion(self, criterion_id):
        for criterion in self.rubrics:
            if criterion.id == criterion_id:
                return criterion
        return None

    @staticmethod
    def from_dict(data_dict):
        if 'submission_types' in data_dict:
            new = Assignment(data_dict['id'], data_dict['name'], data_dict['group_id'], data_dict['section_id'],
                             data_dict['grading_type'], data_dict['grading_standard_id'], data_dict['points'],
                             data_dict['submission_types'],
                             get_date_time_obj(data_dict['assignment_date']),
                             get_date_time_obj(data_dict['unlock_date']),
                             data_dict['assignment_day'], data_dict['unlock_day'])
        else:
            new = Assignment(data_dict['id'], data_dict['name'], data_dict['group_id'], data_dict['section_id'],
                             data_dict['grading_type'], data_dict['grading_standard_id'], data_dict['points'],
                             [],
                             get_date_time_obj(data_dict['assignment_date']),
                             get_date_time_obj(data_dict['unlock_date']),
                             data_dict['assignment_day'], data_dict['unlock_day'])
        new.rubrics = list(map(lambda c: Criterion.from_dict(c), data_dict['rubrics']))
        if 'learning_outcomes' in data_dict:
            new.learning_outcomes = data_dict['learning_outcomes']
        if 'sections' in data_dict:
            new.sections = data_dict['sections']
        if 'messages' in data_dict:
            new.messages = data_dict['messages']
        return new

from model.Student import *


class Students:
    def __init__(self):
        self.students = {}

    def to_json(self, scope):
        return {
            'students': list(map(lambda s: s.to_json(scope), self.students)),
        }

    @staticmethod
    def from_dict(data_dict):
        new_students = Students()
        new_students.students = list(map(lambda s: Student.from_dict(s), data_dict['students']))
        return new_students

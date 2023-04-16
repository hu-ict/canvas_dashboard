from model.AssignmentGroup import AssignmentGroup
from model.Statistics import Statistics
from model.Student import *
from model.StudentGroup import StudentGroup

class Students:
    def __init__(self, pid, name):
        self.students = {}
        self.name = name
        self.id = pid

    def to_json(self, scope):
        return {
            'name': self.name,
            'id': self.id,
            'students': list(map(lambda s: s.to_json(["submission"]), self.students.values())),
        }

    @staticmethod
    def from_dict(data_dict):
        new_students = Students(data_dict['id'], data_dict['name'], data_dict['actual_date'])
        new_students.students = list(map(lambda s: Student.from_dict(s), data_dict['students']))
        return new_students

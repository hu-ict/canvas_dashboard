from model.Assessor import Assessor
from model.StudentLink import StudentLink


class StudentGroup:
    def __init__(self, student_group_id, name, principal_assessor):
        self.id = student_group_id
        self.name = name
        self.principal_assessor = principal_assessor
        self.assessors = []
        self.students = []

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'principal_assessor': self.principal_assessor,
            'assessors': list(map(lambda a: a.to_json(), self.assessors)),
            'students': list(map(lambda s: s.to_json(), self.students))
        }

    def __str__(self):
        line = f'StudentGroup({self.id}, {self.name})'
        for a in self.assessors:
            line += " a "+str(a)
        for s in self.students:
            line += " s "+str(s)
        return line

    @staticmethod
    def from_dict(data_dict):
        new_student_group = StudentGroup(data_dict['id'], data_dict['name'], data_dict['principal_assessor'])
        new_student_group.assessors = list(map(lambda a: Assessor.from_dict(a), data_dict['assessors']))
        new_student_group.students = list(map(lambda s: StudentLink.from_dict(s), data_dict['students']))
        return new_student_group



from model.StudentGroup import StudentGroup
from model.teacher import AssignmentGroupNameId
from model.teacher.Teacher import Teacher


class ResponsibilityMatrix:
    def __init__(self, name):
        self.name = name
        self.teachers = []
        self.student_groups = []
        self.assignment_groups = []


    def to_json(self):
        return {
            'name': self.name,
            'teachers': list(map(lambda t: t.to_json(), self.teachers)),
            'student_groups': list(map(lambda s: s.to_json(), self.student_groups)),
            'assignment_groups': list(map(lambda g: g.to_json(), self.assignment_groups))
        }

    def __str__(self):
        return f'ResponsibilityMatrix({self.name})'

    @staticmethod
    def from_dict(data_dict):
        new = ResponsibilityMatrix(data_dict['name'])
        new.teachers = list(map(lambda t: Teacher.from_dict(t), data_dict['teachers']))
        new.student_groups = list(map(lambda t: StudentGroup.from_dict(t), data_dict['student_groups']))
        new.assignment_groups = list(map(lambda t: AssignmentGroupNameId.from_dict(t), data_dict['assignment_groups']))
        return new

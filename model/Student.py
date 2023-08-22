from model.Perspective import Perspective
from model.StudentPerspective import StudentPerspective
from model.Submission import Submission

class Student:
    def __init__(self, student_id, group_id, name, coach_initials, roles=None):
        self.id = student_id
        self.group_id = group_id
        self.name = name
        self.coach_initials = coach_initials
        self.roles = []
        self.perspectives = []

    def get_role(self):
        if len(self.roles) >= 1:
            for role in self.roles:
                if role != "INNO":
                    return role
            return None
        else:
            return None

    def get_perspective(self, name):
        for perspective in self.perspectives:
            if perspective.name == name:
                return perspective
        return None

    def get_peilmoment(self, assigment_id):
        for peilmoment in self.get_perspective("peil").submissions:
            if peilmoment.assignment_id == assigment_id:
                return peilmoment
        return None

    def to_json(self, scope):
        if "submission" in scope:
            return {
                'name': self.name,
                'id': self.id,
                'group_id': self.group_id,
                'coach_initials': self.coach_initials,
                'roles': self.roles,
                'perspectives': list(map(lambda p: p.to_json(), self.perspectives))
            }
        else:
            return {
                'name': self.name,
                'id': self.id,
                'group_id': self.group_id,
                'coach_initials': self.coach_initials,
                'roles': self.roles
            }

    def __str__(self):
        line = f'Student({self.id}, {self.group_id}, {self.name}, {self.coach_initials}, {self.roles}'
        for perspective in self.perspectives:
            line += " p "+str(perspective)
        return line

    @staticmethod
    def from_dict(data_dict):
        new_student = Student(data_dict['id'], data_dict['group_id'], data_dict['name'], data_dict['coach_initials'])
        new_student.roles = new_student.roles + data_dict['roles']
        new_student.perspectives = list(map(lambda p: StudentPerspective.from_dict(p), data_dict['perspectives']))
        return new_student

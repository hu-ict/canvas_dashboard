from model.Submission import Submission

class Student:
    def __init__(self, student_id, group_id, name, coach_initials, roles=None):
        self.id = student_id
        self.group_id = group_id
        self.name = name
        self.coach_initials = coach_initials
        self.peilmomenten = {}
        self.team = {}
        self.gilde = {}
        self.kennis = {}
        self.roles = []
        self.assignments = {}

    def get_role(self):
        for role in self.roles:
            if role != "INNO":
                return role
        return "None"

    def get_peilmoment(self, assigment_id):
        for peilmoment in self.peilmomenten:
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
                'peilmomenten': list(map(lambda p: p.to_json(), self.peilmomenten.values())),
                'team': list(map(lambda a: a.to_json(), self.team.values())),
                'gilde': list(map(lambda a: a.to_json(), self.gilde.values())),
                'kennis': list(map(lambda a: a.to_json(), self.kennis.values()))
            }
        else:
            return {
                'name': self.name,
                'id': self.id,
                'group_id': self.group_id,
                'coach_initials': self.coach_initials,
                'roles': self.roles
                ,
                # 'peilmomenten': [],
                # 'team': [],
                # 'gilde': [],
                # 'kennis': []
            }

    def __str__(self):
        line = f'Student({self.id}, {self.group_id}, {self.name}, {self.coach_initials}, {self.roles}'
        for b in self.peilmomenten:
            line += "\n b "+str(b)
        for t in self.team:
            line += "\n t "+str(t)
        for g in self.gilde:
            line += "\n g "+str(g)
        for k in self.kennis:
            line += "\n k "+str(k)
        return line

    @staticmethod
    def from_dict(data_dict):
        new_student = Student(data_dict['id'], data_dict['group_id'], data_dict['name'], data_dict['coach_initials'])
        new_student.roles = new_student.roles + data_dict['roles']
        new_student.peilmomenten = list(map(lambda b: Submission.from_dict(b), data_dict['peilmomenten']))
        new_student.team = list(map(lambda t: Submission.from_dict(t), data_dict['team']))
        new_student.gilde = list(map(lambda g: Submission.from_dict(g), data_dict['gilde']))
        new_student.kennis = list(map(lambda k: Submission.from_dict(k), data_dict['kennis']))
        return new_student
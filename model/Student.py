from model.Assessor import Assessor


class Student:
    def __init__(self, a_student_id, a_project_id, a_guild_id, a_name, a_number, a_sortable_name, a_role, a_email, a_site, principal_assessor):
        self.id = a_student_id
        self.project_id = a_project_id
        self.guild_id = a_guild_id
        self.name = a_name
        self.number = a_number
        self.sortable_name = a_sortable_name
        self.principal_assessor = principal_assessor
        self.guild_teachers = []
        self.email = a_email
        self.site = a_site
        self.role = a_role
        self.assessors = []

    def __str__(self):
        line = f'Student({self.id}, {self.project_id}, {self.guild_id}, {self.name}, {self.number}, {self.principal_assessor}, {self.guild_teachers}, {self.role}, {self.email}, {self.assessors})'
        return line

    def to_json(self):
        dict_result = {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'sortable_name': self.sortable_name,
            'role': self.role,
            'project_id': self.project_id,
            'guild_id': self.guild_id,
            'principal_assessor': self.principal_assessor,
            'guild_teachers': self.guild_teachers,
            'assessors': list(map(lambda a: a.to_json(), self.assessors)),
            'email': self.email,
            'site': self.site
        }
        return dict_result

    def get_assessor_by_assignment_group(self, assignment_group_id):
        for assessor in self.assessors:
            if assessor.assignment_group_id == assignment_group_id:
                return assessor
        return None

    @staticmethod
    def from_dict(data_dict):
        new = Student(data_dict['id'], data_dict['project_id'], data_dict['guild_id'], data_dict['name'],
                      data_dict['number'], data_dict['sortable_name'],
                      data_dict['role'], data_dict['email'], data_dict['site'],
                      data_dict['principal_assessor'])
        if 'guild_teachers' in data_dict:
            new.guild_teachers = data_dict['guild_teachers']
        if 'assessors' in data_dict:
            new.assessors = list(map(lambda a: Assessor.from_dict(a), data_dict['assessors']))
        return new

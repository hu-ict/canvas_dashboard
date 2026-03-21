from scripts.model.Assessor import Assessor


class Student:
    def __init__(self, a_student_id, groups_1_group_id, groups_2_group_id, a_name, a_number, a_sortable_name, a_role, a_section, a_email, a_site):
        self.id = a_student_id
        self.groups_1_group_id = groups_1_group_id
        self.groups_2_group_id = groups_2_group_id
        self.name = a_name
        self.number = a_number
        self.sortable_name = a_sortable_name
        self.email = a_email
        self.site = a_site
        self.role = a_role
        self.section = a_section
        self.assessors = []

    def __str__(self):
        line = f'Student({self.id}, {self.groups_1_group_id}, {self.groups_2_group_id}, {self.name}, {self.number}, {self.role}, {self.email}, {self.assessors})'
        return line

    def to_json(self):
        dict_result = {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'sortable_name': self.sortable_name,
            'role': self.role,
            'section': self.section,
            'groups_1_group_id': self.groups_1_group_id,
            'groups_2_group_id': self.groups_2_group_id,
            'email': self.email,
            'site': self.site,
            'assessors': list(map(lambda a: a.to_json(), self.assessors))
        }
        return dict_result

    def get_assessor_by_assignment_group(self, assignment_group_id):
        for assessor in self.assessors:
            if assessor.assignment_group_id == assignment_group_id:
                return assessor
        return None

    @staticmethod
    def from_dict(data_dict):
        new = Student(data_dict['id'], data_dict['groups_1_group_id'], data_dict['groups_2_group_id'], data_dict['name'],
                      data_dict['number'], data_dict['sortable_name'],
                      data_dict['role'], data_dict['section'], data_dict['email'], data_dict['site'])
        if 'assessors' in data_dict:
            new.assessors = list(map(lambda a: Assessor.from_dict(a), data_dict['assessors']))
        return new

class Student:
    def __init__(self, a_student_id, a_group_id, a_name, a_number, a_sortable_name, a_coach, a_role, a_email, a_site):
        self.id = a_student_id
        self.group_id = a_group_id
        self.name = a_name
        self.number = a_number
        self.sortable_name = a_sortable_name
        self.coach = a_coach
        self.email = a_email
        self.site = a_site
        self.role = a_role

    def __str__(self):
        line = f'Student({self.id}, {self.group_id}, {self.name}, {self.number}, {self.coach}, {self.role}, {self.email})\n'
        return line

    def to_json(self):
        dict_result = {
            'name': self.name,
            'id': self.id,
            'number': self.number,
            'sortable_name': self.sortable_name,
            'group_id': self.group_id,
            'role': self.role,
            'coach': self.coach,
            'email': self.email,
            'site': self.site
        }
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        new = Student(data_dict['id'], data_dict['group_id'], data_dict['name'], data_dict['number'],
                      data_dict['sortable_name'], data_dict['coach'],
                      data_dict['role'], data_dict['email'], data_dict['site'])
        return new

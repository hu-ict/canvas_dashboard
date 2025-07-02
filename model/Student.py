class Student:
    def __init__(self, a_student_id, a_project_id, a_guild_id, a_name, a_number, a_sortable_name, a_role, a_email, a_site):
        self.id = a_student_id
        self.project_id = a_project_id
        self.guild_id = a_guild_id
        self.name = a_name
        self.number = a_number
        self.sortable_name = a_sortable_name
        self.project_teachers = []
        self.guild_teachers = []
        self.email = a_email
        self.site = a_site
        self.role = a_role

    def __str__(self):
        line = f'Student({self.id}, {self.project_id}, {self.guild_id}, {self.name}, {self.number}, {self.project_teachers}, {self.guild_teachers}, {self.role}, {self.email})'
        return line

    def to_json(self):
        dict_result = {
            'name': self.name,
            'id': self.id,
            'number': self.number,
            'sortable_name': self.sortable_name,
            'project_id': self.project_id,
            'guild_id': self.guild_id,
            'role': self.role,
            'project_teachers': self.project_teachers,
            'guild_teachers': self.guild_teachers,
            'email': self.email,
            'site': self.site
        }
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        if 'project_id' in data_dict:
            project_id = data_dict['project_id']
        else:
            project_id = data_dict['group_id']
        if 'guild_id' in data_dict:
            guild_id = data_dict['guild_id']
        else:
            guild_id = None
        new = Student(data_dict['id'], project_id, guild_id, data_dict['name'],
                      data_dict['number'], data_dict['sortable_name'],
                      data_dict['role'], data_dict['email'], data_dict['site'])
        if 'project_teachers'in data_dict:
            project_teachers = data_dict['project_teachers']
        else:
            project_teachers = [data_dict['coach']]
        if 'guild_teachers' in data_dict:
            guild_teachers = data_dict['guild_teachers']
        new.project_teachers = project_teachers
        new.guild_teachers = guild_teachers
        return new

from model.Responsibility import Responsibility


class Teacher:
    def __init__(self, teacher_id, name, email):
        self.id = teacher_id
        self.name = name
        self.initials = ''.join([x[0].upper() for x in name.split(' ')])
        self.email = email
        self.project_groups = []
        self.guild_groups = []
        self.responsibilities = []

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'project_groups': self.project_groups,
            'guild_groups': self.guild_groups,
            'responsibilities': list(map(lambda r: r.to_json(), self.responsibilities))
        }

    def __str__(self):
        return f'Teacher({self.id}, {self.name}, {self.initials}, {self.email}, {self.project_groups}, {self.guild_groups})'

    @staticmethod
    def from_dict(data_dict):
        if 'email' in data_dict:
            new_teacher = Teacher(data_dict['id'], data_dict['name'], data_dict["email"])
        else:
            new_teacher = Teacher(data_dict['id'], data_dict['name'], "")
        if 'project_groups' in data_dict:
            new_teacher.project_groups = data_dict['project_groups']
        else:
            new_teacher.project_groups = data_dict['teams']
        if 'guild_groups' in data_dict:
            new_teacher.guild_groups = data_dict['guild_groups']
        if 'responsibilities' in data_dict:
            # print("TE41 - read responsibilities", new_teacher.name, data_dict['responsibilities'])
            new_teacher.responsibilities = list(map(lambda r: Responsibility.from_dict(r), data_dict['responsibilities']))
        return new_teacher

class Teacher:
    def __init__(self, teacher_id, name, email):
        self.id = teacher_id
        self.name = name
        self.initials = ''.join([x[0].upper() for x in name.split(' ')])
        self.email = email
        self.teams = []


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'teams': self.teams,
        }

    def __str__(self):
        return f'Teacher({self.id}, {self.name}, {self.initials}, {self.email}, {self.teams}'

    @staticmethod
    def from_dict(data_dict):
        if 'email' in data_dict:
            new_teacher = Teacher(data_dict['id'], data_dict['name'], data_dict["email"])
        else:
            new_teacher = Teacher(data_dict['id'], data_dict['name'], "")
        new_teacher.teams = data_dict['teams']
        return new_teacher

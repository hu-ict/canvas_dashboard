class Teacher:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.initials = ''.join([x[0].upper() for x in name.split(' ')])
        self.login_id = ""
        self.teams = []


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'login_id': self.login_id,
            'teams': self.teams,
        }

    def __str__(self):
        return f'Teacher({self.id}, {self.name}, {self.initials}, {self.login_id}, {self.teams}'

    @staticmethod
    def from_dict(data_dict):
        new_teacher = Teacher(data_dict['id'], data_dict['name'])
        if 'login_id' in data_dict:
            new_teacher.email = data_dict['login_id']
        new_teacher.teams = data_dict['teams']
        return new_teacher

class Teacher:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.initials = ''.join([x[0].upper() for x in name.split(' ')])
        self.login_id = ""
        self.teams = []

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'login_id': self.login_id,
            'teams': self.teams,
            'email': self.email
        }

    def __str__(self):
        return f'Teacher({self.id}, {self.name}, {self.initials}, {self.login_id}, {self.teams}, {self.email})'

    @staticmethod
    def from_dict(data_dict):
        email = data_dict.get('email', '')  # Provide a default value for email
        new_teacher = Teacher(data_dict['id'], data_dict['name'], email)
        return new_teacher
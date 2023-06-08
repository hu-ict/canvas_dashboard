class Teacher:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.initials = ''.join([x[0].upper() for x in name.split(' ')])
        self.projects = []
        self.assignment_groups = []

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'initials': self.initials,
            'projects': self.projects,
            'assignment_groups': self.assignment_groups
        }

    def __str__(self):
        return f'Teacher({self.id}, {self.name}, {self.initials}, {self.projects}, {self.assignment_groups}'

    @staticmethod
    def from_dict(data_dict):
        new_teacher = Teacher(data_dict['id'], data_dict['name'])
        new_teacher.projects = data_dict['projects']
        new_teacher.assignment_groups = data_dict['assignment_groups']
        return new_teacher

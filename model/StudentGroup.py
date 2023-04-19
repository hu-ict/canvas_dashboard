class StudentGroup:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.teachers = []
        self.students = []

    def to_json(self, scope):
        return {
            'id': self.id,
            'name': self.name,
            'teachers': self.teachers,
            'students': list(map(lambda s: s.to_json(scope), self.students)),
        }

    def __str__(self):
        return f'StudentGroup({self.id}, {self.name}, {self.teachers})\n'

    @staticmethod
    def from_dict(data_dict):
        new_student_group = StudentGroup(data_dict['id'], data_dict['name'])
        new_student_group.teachers = data_dict['teachers']
        return new_student_group


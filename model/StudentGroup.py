class StudentGroup:
    def __init__(self, id, name, coach):
        self.id = id
        self.name = name
        self.coach = coach
        self.students = []

    def to_json(self, scope):
        return {
            'id': self.id,
            'name': self.name,
            'coach': self.coach,
            'students': list(map(lambda s: s.to_json(scope), self.students)),
        }

    def __str__(self):
        return f'StudentGroup({self.id}, {self.name}, {self.coach})'

    @staticmethod
    def from_dict(data_dict):
        return StudentGroup(data_dict['id'], data_dict['name'], data_dict['coach'])

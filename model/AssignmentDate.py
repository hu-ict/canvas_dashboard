class AssignmentDate:
    def __init__(self, id, due_at, lock_at):
        self.id = id
        self.due_at = due_at
        self.lock_at = lock_at

    def to_json(self):
        return {
            'id': self.id,
            'due_at': self.due_at,
            'lock_at': self.lock_at,
        }

    def __str__(self):
        return f'AssigmentDate({self.id}, {self.due_at}, {self.lock_at})'

    @staticmethod
    def from_dict(data_dict):
        return AssignmentDate(data_dict['id'], data_dict['due_at'], data_dict['lock_at'])

class LearningOutcome:
    def __init__(self, id, short, description):
        self.id = id
        self.short = short
        self.description = description

    def to_json(self):
        return {
            'id': self.id,
            'short': self.short,
            'description': self.description
        }

    def __str__(self):
        return f'LearningOutcome(Id: {self.id}, {self.short}, {self.description})'

    @staticmethod
    def from_dict(data_dict):
        new = LearningOutcome(data_dict['id'], data_dict['short'], data_dict['description'])
        return new

class LearningOutcome:
    def __init__(self, id, short, description):
        self.id = id
        self.short = short
        self.description = description
        self.assignment_sequences = []

    def to_json(self):
        return {
            'id': self.id,
            'short': self.short,
            'description': self.description,
            'assignment_sequences': self.assignment_sequences
        }

    def add_assigment_sequence(self, tag):
        if tag not in self.assignment_sequences:
            self.assignment_sequences.append(tag)

    def __str__(self):
        return f'LearningOutcome(Id: {self.id}, {self.short}, {self.description})'

    @staticmethod
    def from_dict(data_dict):
        new = LearningOutcome(data_dict['id'], data_dict['short'], data_dict['description'])
        if 'assignment_sequences' in data_dict:
            new.assignment_sequences = data_dict['assignment_sequences']
        return new

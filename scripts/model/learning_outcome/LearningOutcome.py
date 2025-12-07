class LearningOutcome:
    def __init__(self, learning_outcome_id, short, description):
        self.id = learning_outcome_id
        self.short = short
        self.description = description
        self.min_items = None
        self.min_score = None
        self.above_items = None
        self.above_score = None
        self.assignment_sequences = []

    def to_json(self):
        return {
            'id': self.id,
            'short': self.short,
            'description': self.description,
            'min_items': self.min_items,
            'min_score': self.min_score,
            'above_items': self.above_items,
            'above_score': self.above_score,
            'assignment_sequences': self.assignment_sequences
        }

    def add_assigment_sequence(self, assigment_sequence_tag):
        if assigment_sequence_tag not in self.assignment_sequences:
            self.assignment_sequences.append(assigment_sequence_tag)

    def add_criterion_id(self, assigment_sequence_tag, criterion_id):
        if criterion_id not in self.assignment_sequences:
            self.assignment_sequences.append(assigment_sequence_tag+":"+criterion_id)

    def add_assignment_tag_id(self, assigment_sequence_tag):
        if assigment_sequence_tag not in self.assignment_sequences:
            self.assignment_sequences.append(assigment_sequence_tag)

    def get_grade(self, items, score):
        if items == 0:
            return "0"
        grade = "1"
        if self.min_items is not None:
            if items >= self.min_items:
                grade = "2"
            if items >= self.above_items:
                grade = "3"
        elif self.min_score is not None:
            if score >= self.min_score:
                grade = "2"
            if score >= self.above_score:
                grade = "3"
        return grade


    def __str__(self):
        return f'LearningOutcome(Id: {self.id}, {self.short}, {self.description})'

    @staticmethod
    def from_dict(data_dict):
        new = LearningOutcome(data_dict['id'], data_dict['short'], data_dict['description'])
        if 'min_items' in data_dict:
            new.min_items = data_dict['min_items']
            new.above_items = data_dict['above_items']
        if 'min_score' in data_dict:
            new.min_score = data_dict['min_score']
            new.above_score = data_dict['above_score']
        if 'assignment_sequences' in data_dict:
            new.assignment_sequences = data_dict['assignment_sequences']
        return new

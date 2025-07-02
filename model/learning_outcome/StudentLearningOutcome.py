from model.learning_outcome.Feedback import Feedback


class StudentLearningOutcome:
    def __init__(self, learning_outcome_id, short):
        self.id = learning_outcome_id
        self.short = short
        self.feedback_list = []

    def to_json(self):
        return {
            'id': self.id,
            'short': self.short,
            'feedback_list': list(map(lambda f: f.to_json(), self.feedback_list))
        }

    def __str__(self):
        return f'StudentLearningOutcome(Id: {self.id}, {self.short}, {len(self.feedback_list)})'

    @staticmethod
    def from_dict(data_dict):
        new = StudentLearningOutcome(data_dict['id'], data_dict['short'])
        for feedback in data_dict['feedback_list']:
            new.feedback_list.append(Feedback.from_dict(feedback))
        return new

    @staticmethod
    def copy_from(learning_outcome):
        return StudentLearningOutcome(learning_outcome.id, learning_outcome.short)
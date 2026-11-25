from scripts.model.learning_outcome.Feedback import Feedback
from scripts.model.learning_outcome.SaturationDay import SaturationDay

class StudentLearningOutcome:
    def __init__(self, learning_outcome_id, short, saturation):
        self.id = learning_outcome_id
        self.short = short
        self.saturation = saturation
        self.feedback_list = []

    def to_json(self):
        return {
            'id': self.id,
            'short': self.short,
            'saturation': self.saturation,
            'feedback_list': list(map(lambda f: f.to_json(), self.feedback_list))
        }

    def __str__(self):
        return f'StudentLearningOutcome(Id: {self.id}, {self.short}, {self.saturation}, {len(self.feedback_list)})'

    def get_saturation_day_list(self, actual_day):
        item_saturation_day_list = []
        for day in range(actual_day+1):
            item_saturation_day_list.append(SaturationDay(day, 0))
        for feedback in self.feedback_list:
            item_saturation_day_list[feedback.day].value += 1
        cumulative = 0
        cum_saturation_day_list = []
        for day in range(actual_day+1):
            cumulative += item_saturation_day_list[day].value
            cum_saturation_day_list.append(SaturationDay(day, cumulative))
        return cum_saturation_day_list

    @staticmethod
    def from_dict(data_dict):
        new = StudentLearningOutcome(data_dict['id'], data_dict['short'], data_dict['saturation'])
        for feedback in data_dict['feedback_list']:
            new.feedback_list.append(Feedback.from_dict(feedback))
        return new

    @staticmethod
    def copy_from(learning_outcome):
        return StudentLearningOutcome(learning_outcome.id, learning_outcome.short, 0)
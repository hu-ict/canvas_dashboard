from scripts.model.learning_outcome.Feedback import Feedback
from scripts.model.learning_outcome.SaturationStatistics import SaturationStatistics


class SaturationLearningOutcome:
    def __init__(self, learning_outcome_id, short):
        self.id = learning_outcome_id
        self.short = short
        self.last_day_collection = []
        self.days = []

    def to_json(self):
        return {
            'id': self.id,
            'short': self.short,
            'last_day_collection': self.last_day_collection,
            'days': list(map(lambda d: d.to_json(), self.days))
        }

    def __str__(self):
        return f'SaturationLearningOutcome(Id: {self.id}, {self.short}, {len(self.days)})'

    def get_day(self, day):
        for d in self.days:
            if d.day == day:
                return d
        return None

    @staticmethod
    def from_dict(data_dict):
        new = SaturationLearningOutcome(data_dict['id'], data_dict['short'])
        new.last_day_collection = data_dict['last_day_collection']
        for day in data_dict['days']:
            new.days.append(SaturationStatistics.from_dict(day))
        return new

from scripts.model.learning_outcome.Feedback import Feedback

class SaturationStatistics:
    def __init__(self, learning_outcome_id, short, day, low, min_stdv, average, plus_stdv, high):
        self.id = learning_outcome_id
        self.short = short
        self.day = day
        self.average = average
        self.high = high
        self.low = low
        self.plus_stdv = plus_stdv
        self.min_stdv = min_stdv
        self.collection = []

    def to_json(self):
        return {
            'id': self.id,
            'short': self.short,
            'day': self.day,
            'average': self.average,
            'high': self.high,
            'low': self.low,
            'plus_stdv': self.plus_stdv,
            'min_stdv': self.min_stdv
        }

    def __str__(self):
        return f'SaturationStatistics(Id: {self.id}, Short: {self.short}, Day: {self.day}, Low: {self.low}, {self.min_stdv}, Average: {self.average}, {self.plus_stdv}, {self.high})'

    @staticmethod
    def from_dict(data_dict):
        new = SaturationStatistics(data_dict['id'], data_dict['short'], data_dict['day'], data_dict['low'], data_dict['min_stdv'], data_dict['average'], data_dict['plus_stdv'], data_dict['high'])
        return new

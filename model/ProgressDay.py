class ProgressDay:
    def __init__(self, day):
        self.day = day
        self.progress = {"-1": 0, "0": 0, "1": 0, "2": 0, "3": 0}

    def to_json(self):
        return {
            'day': self.day,
            'progress': self.progress
        }

    def __str__(self):
        return f'ProgressDay({self.day}, {self.progress})\n'

    @staticmethod
    def from_dict(data_dict):
        new = ProgressDay(data_dict['day'])
        new.progress = data_dict['progress']
        return new


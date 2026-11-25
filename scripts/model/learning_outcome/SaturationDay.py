class SaturationDay:
    def __init__(self, day, value):
        self.day = day
        self.value = value

    def to_json(self):
        return {
            'day': self.day,
            'value': self.value
        }

    def __str__(self):
        return f'SaturationDay({self.day}, {self.value})'

    @staticmethod
    def from_dict(data_dict):
        new = SaturationDay(data_dict['day'], data_dict['value'])
        return new

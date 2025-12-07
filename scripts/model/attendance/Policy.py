class Policy:
    def __init__(self, starting_days, recurring, times, exceptions):
        self.starting_days = starting_days
        self.recurring = recurring
        self.times = times
        self.exceptions = exceptions

    def to_json(self):
        dict_result = {
            'starting_days': self.starting_days,
            'recurring': self.recurring,
            'times': self.times,
            'exceptions': self.exceptions
        }
        return dict_result

    def __str__(self):
        return f'Policy({self.starting_days}, {self.recurring}, {self.times}, {self.exceptions})'

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        new = Policy(data_dict['starting_days'], data_dict['recurring'], data_dict['times'], data_dict['exceptions'])
        return new

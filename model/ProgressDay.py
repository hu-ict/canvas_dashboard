class ProgressDay:
    def __init__(self, day, perspectives):
        self.day = day
        self.progress = {"-2": 0, "-1": 0, "0": 0, "1": 0, "2": 0, "3": 0}
        self.attendance = {"-2": 0, "-1": 0, "0": 0, "1": 0, "2": 0, "3": 0}
        self.perspective = {}
        for perspective in perspectives:
            self.perspective[perspective] = {"-2": 0, "-1": 0, "0": 0, "1": 0, "2": 0, "3": 0}

    def to_json(self):
        return {
            'day': self.day,
            'progress': self.progress,
            'attendance': self.attendance,
            'perspective': self.perspective
        }

    def __str__(self):
        return f'ProgressDay({self.day}, {self.progress}, {self.progress}, {self.perspective})\n'

    @staticmethod
    def from_dict(data_dict):
        new = ProgressDay(data_dict['day'], {})
        new.progress = data_dict['progress']
        if 'attendance' in data_dict.keys() and data_dict['attendance'] is not None:
            new.attendance = data_dict['attendance']
        if "-2" not in new.progress.keys():
            new.progress["-2"] = 0
        if "perspective" in data_dict:
            new.perspective = data_dict['perspective']
        return new


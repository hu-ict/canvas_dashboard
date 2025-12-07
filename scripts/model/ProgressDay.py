class ProgressDay:
    def __init__(self, day, course_perspectives):
        self.day = day
        self.progress = {"-2": 0, "-1": 0, "0": 0, "1": 0, "2": 0, "3": 0}
        self.attendance = {"-2": 0, "-1": 0, "0": 0, "1": 0, "2": 0, "3": 0}
        self.perspectives = {}
        for perspective in course_perspectives:
            self.perspectives[perspective] = {"-2": 0, "-1": 0, "0": 0, "1": 0, "2": 0, "3": 0}

    def to_json(self):
        return {
            'day': self.day,
            'progress': self.progress,
            'attendance': self.attendance,
            'perspectives': self.perspectives
        }

    def __str__(self):
        return f'ProgressDay({self.day}, progress {self.progress}, attendance {self.attendance}, {self.perspectives})\n'

    @staticmethod
    def from_dict(data_dict):
        new = ProgressDay(data_dict['day'], {})
        new.progress = data_dict['progress']
        if 'attendance' in data_dict.keys() and data_dict['attendance'] is not None:
            new.attendance = data_dict['attendance']
        if "-2" not in new.progress.keys():
            new.progress["-2"] = 0
        if "perspectives" in data_dict:
            new.perspectives = data_dict['perspectives']
        return new


class Point:
    def __init__(self, day, lower, upper):
        self.day = day
        self.lower = lower
        self.upper = upper

    def to_json(self):
        return {
            'day': self.day,
            'lower': int(self.lower*100)/100,
            'upper': int(self.upper*100)/100
        }

    def __str__(self):
        return f'Point({self.day}, {self.lower}, {self.upper})'

    @staticmethod
    def from_dict(data_dict):
        return Point(data_dict['day'], data_dict['lower'], data_dict['upper'])


class Bandwidth:
    def __init__(self):
        self.days = []
        self.lowers = []
        self.uppers = []
        self.points = []

    def to_json(self):
        return {
            'days': self.days,
            'lowers': list(map(lambda u: int(u*100)/100, self.lowers)),
            'uppers': list(map(lambda u: int(u*100)/100, self.uppers)),
            'points': list(map(lambda p: p.to_json(), self.points))
        }

    def __str__(self):
        line = f'Bandwidth({self.lowers})'
        for point in self.points:
            line += str(point)
        return line

    def get_progress(self, strategy, this_day, day, score):
        if day == 0:
            return -1
        elif score == 0:
            return 0
        else:
            pass
        try:
            if strategy == "FIXED":
                day = this_day
            if type(day) == str:
                day = int(day)
            if score < self.points[day].lower:
                return 1
            elif score < self.points[day].upper:
                return 2
            else:
                return 3
        except IndexError:
            if score < self.points[len(self.points)-1].lower:
                return 1
            elif score < self.points[len(self.points)-1].upper:
                return 2
            else:
                return 3

    def get_progress_range(self, day, score):
        if day == 0:
            return -1
        elif score == 0:
            return 0
        else:
            pass
        try:
            if type(day) == str:
                day = int(day)
            width = self.points[day].upper - self.points[day].lower
            if score < self.points[day].lower:
                return score / self.points[day].lower * 3/10
            elif score < self.points[day].upper:
                return 0.3 + (score - self.points[day].lower) / width * 4/10
            else:
                return 0.7 + (score - self.points[day].upper) / width * 3/10
        except IndexError:
            if score < self.points[len(self.points)-1].lower:
                return 1
            elif score < self.points[len(self.points)-1].upper:
                return 2
            else:
                return 3


    @staticmethod
    def from_dict(data_dict):
        if data_dict is None:
            return None
        new = Bandwidth()
        new.days = data_dict['days']
        new.lowers = data_dict['lowers']
        new.uppers = data_dict['uppers']
        new.points = list(map(lambda p: Point.from_dict(p), data_dict['points']))
        return new

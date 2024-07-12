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
            'points': list(map(lambda p: p.to_json(), self.points))
        }

    def __str__(self):
        line = f'Bandwidth({self.lowers})'
        for point in self.points:
            line += str(point)
        return line

    def get_progress(self, day, score):
        if day == 0:
            return -1
        elif score == 0:
            return 0
        else:
            pass
        try:
            day = int(day)
            if score < self.points[day].lower:
                # print(score, "<", self.points[day].lower, 1)
                return 1
            elif score < self.points[day].upper:
                return 2
            else:
                return 3
        except IndexError:
            if score < self.points[len(self.points)-1].lower:
                # print(score, "<", self.points[day].lower, 1, "exception")
                return 1
            elif score < self.points[len(self.points)-1].upper:
                return 2
            else:
                return 3

    def get_progress_range(self, day, score):
        if day <= 0:
            return -1
        elif score == 0:
            return 0
        else:
            pass
        if type(day) == str:
            day = int(day)
        if day > len(self.points)-1:
            day = len(self.points)-1
        width = self.points[day].upper - self.points[day].lower
        print("BW03 -", self.points[day].upper, self.points[day].lower)
        if score < self.points[day].lower:
            return score / self.points[day].lower * 3/10
        elif score < self.points[day].upper:
            return 0.3 + (score - self.points[day].lower) / width * 4/10
        else:
            flow = 0.7 + (score - self.points[day].upper) / width * 3/10
            if flow > 0.97:
                # anders lopen de datapunten en het plaatje uit.
                return 0.97
            return flow


    @staticmethod
    def from_dict(data_dict):
        if data_dict is None:
            return None
        new = Bandwidth()
        new.points = list(map(lambda p: Point.from_dict(p), data_dict['points']))
        for point in new.points:
            new.lowers.append(point.lower)
            new.uppers.append(point.upper)
            new.days.append(point.day)

        return new

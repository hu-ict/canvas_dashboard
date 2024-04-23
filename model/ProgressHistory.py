from model.ProgressDay import ProgressDay


class ProgressHistory:
    def __init__(self):
        self.days = []

    def find_day_index(self, day):
        i = 0
        for d in self.days:
            if d.day == day:
                return i
            i += 1
        return None


    def get_day(self, day):
        for d in self.days:
            if d.day == day:
                return d
        return None


    def append_day(self, progress_day):
        index = self.find_day_index(progress_day.day)
        if index is None:
            # voeg toe
            self.days.append(progress_day)
        else:
            # vervang
            self.days[index] = progress_day

    def to_json(self):
        return {
            'days': list(map(lambda d: d.to_json(), self.days))
        }

    def __str__(self):
        line = f'ProgressHistory()\n'
        for d in self.days:
            line += " " + str(d)
        return line

    @staticmethod
    def from_dict(data_dict):
        new = ProgressHistory()
        new.days = list(map(lambda p: ProgressDay.from_dict(p), data_dict['days']))
        return new

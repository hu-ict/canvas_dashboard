from model.WorkloadDay import WorkloadDay


class WorkloadHistory:
    def __init__(self):
        self.days = []

    def __str__(self):
        line = f'WorkloadHistory()\n'
        for d in self.days:
            line += " " + str(d)
        return line

    def to_json(self):
        return {
            'days': list(map(lambda d: d.to_json(), self.days))
        }

    def find_day_index(self, day):
        i = 0
        for d in self.days:
            if d.day == day:
                return i
            i += 1
        return None

    def append_day(self, workload_day):
        index = self.find_day_index(workload_day.day)
        if index is None:
            # voeg toe
            self.days.append(workload_day)
        else:
            # vervang
            self.days[index] = workload_day

    @staticmethod
    def from_dict(data_dict):
        new = WorkloadHistory()
        new.days = list(map(lambda p: WorkloadDay.from_dict(p), data_dict['days']))
        return new

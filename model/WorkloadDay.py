workload_aspects = {"count": 0, "week": 0, "over_week": 0, "over_14": 0}


class WorkloadDay:
    def __init__(self, day):
        self.day = day
        self.workload = workload_aspects

    def to_json(self):
        return {
            'day': self.day,
            'workload': self.workload
        }

    def __str__(self):
        return f'WorkloadDay({self.day}, {self.workload})\n'

    def from_late_list(self, late_list):
        workload_aspects["count"] = len(late_list)
        over_14 = 0
        over_7 = 0
        week = 0
        for item in late_list:
            if item > 14:
                over_14 += 1
            elif item > 7:
                over_7 += 1
            else:
                week += 1
        workload_aspects["week"] = week
        workload_aspects["over_week"] = over_7
        workload_aspects["over_14"] = over_14

    @staticmethod
    def from_dict(data_dict):
        new = WorkloadDay(data_dict['day'])
        new.workload = data_dict['workload']
        return new


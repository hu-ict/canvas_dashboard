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

    def from_actual_workload(self, workload):
        pending = 0
        late = 0
        to_late = 0
        for perspective in workload["perspectives"]:
            for selector in workload["perspectives"][perspective]["pending"]:
                pending += workload["perspectives"][perspective]["pending"][selector]
            for selector in workload["perspectives"][perspective]["late"]:
                late += workload["perspectives"][perspective]["late"][selector]
            for selector in workload["perspectives"][perspective]["to_late"]:
                to_late += workload["perspectives"][perspective]["to_late"][selector]

        workload_aspects["week"] = pending
        workload_aspects["over_week"] = late
        workload_aspects["over_14"] = to_late
        workload_aspects["count"] = pending + late + to_late

    @staticmethod
    def from_dict(data_dict):
        new = WorkloadDay(data_dict['day'])
        new.workload = data_dict['workload']
        return new


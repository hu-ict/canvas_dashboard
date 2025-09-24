class Workload:
    def __init__(self, day):
        self.day = day
        self.workload_teachers = []

    def to_json(self):
        return {
            'day': self.day,
            'workload_teachers': self.workload_teachers
        }

    def __str__(self):
        return f'Workload{self.day}, {self.workload_teachers})\n'

    def get_workload_teacher(self, teacher_id):
        for teacher in self.workload_teachers:
            if teacher.teacher_id == teacher_id:
                return teacher
        return None

    def get_initials(self):
        initials = []
        for teacher in self.workload_teachers:
            initials.append(teacher.initials)
        return initials

    def get_w1_count(self):
        w1_count = []
        for teacher in self.workload_teachers:
            w1_count.append(teacher.w1_count)
        return w1_count

    def get_w2_count(self):
        w2_count = []
        for teacher in self.workload_teachers:
            w2_count.append(teacher.w2_count)
        return w2_count

    def get_w3_count(self):
        w3_count = []
        for teacher in self.workload_teachers:
            w3_count.append(teacher.w3_count)
        return w3_count

    @staticmethod
    def from_dict(data_dict):
        new = Workload(data_dict['day'])
        new.workload = data_dict['workload_teachers']
        return new


class WorkloadTeacher:
    def __init__(self, teacher_id, initials, name, w1_count, w2_count, w3_count):
        self.teacher_id = teacher_id
        self.initials = initials
        self.name = name
        self.w1_count = w1_count
        self.w2_count = w2_count
        self.w3_count = w3_count
        self.worklist = []

    def to_json(self):
        return {
            'teacher_id': self.teacher_id,
            'initials': self.initials,
            'name': self.name,
            'w1_count': self.w1_count,
            'w2_count': self.w2_count,
            'w3_count': self.w3_count,
            'worklist': self.worklist
        }

    def __str__(self):
        return f'WorkloadDay({self.teacher_id}, {self.initials}, {self.name}, {self.worklist})'

    @staticmethod
    def from_dict(data_dict):
        new = WorkloadTeacher(data_dict['teacher_id'], data_dict['initials'], data_dict['name'], data_dict['w1_count'], data_dict['w2_count'], data_dict['w3_count'])
        new.work_list = data_dict['worklist']
        return new


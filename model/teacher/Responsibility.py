class Responsibility:
    def __init__(self, student_group_collection, student_groups, assignment_group_id):
        self.student_group_collection = student_group_collection
        self.student_groups = student_groups
        self.assignment_group_id = assignment_group_id

    def to_json(self):
        return {
            'student_group_collection': self.student_group_collection,
            'student_groups': self.student_groups,
            'assignment_group_id': self.assignment_group_id,
        }

    def __str__(self):
        return f'Responsibility({self.student_group_collection}, {self.student_groups}, {self.assignment_group_id}'

    @staticmethod
    def from_dict(data_dict):
        return Responsibility(data_dict['student_group_collection'], data_dict['student_groups'], data_dict['assignment_group_id'])

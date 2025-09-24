class Assessor:
    def __init__(self, teacher_id, student_group_collection, student_group_id, assignment_group_id):
        self.teacher_id = teacher_id
        self.student_group_collection = student_group_collection
        self.student_group_id = student_group_id
        self.assignment_group_id = assignment_group_id

    def to_json(self):
        return {
            'teacher_id': self.teacher_id,
            'student_group_collection': self.student_group_collection,
            'student_group_id': self.student_group_id,
            'assignment_group_id': self.assignment_group_id,
        }

    def __str__(self):
        return f'Assessor({self.student_group_collection}, {self.student_group_id}, {self.assignment_group_id})'

    @staticmethod
    def from_dict(data_dict):
        return Assessor(data_dict['teacher_id'], data_dict['student_group_collection'], data_dict['student_group_id'], data_dict['assignment_group_id'])

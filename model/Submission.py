from lib.lib_date import get_date_time_obj, get_date_time_str
from model.Comment import Comment

class Submission:
    def __init__(self, submission_id, assignment_group_id, assignment_id, student_id, assignment_name, assignment_date, submitted_date, graded, score, points, flow):
        self.id = submission_id
        self.assignment_group_id = assignment_group_id
        self.assignment_name = assignment_name
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.assignment_date = assignment_date
        self.submitted_date = submitted_date
        self.graded = graded
        self.score = score
        self.points = points
        self.flow = flow
        self.comments = []

    def toJson(self):
        return self.to_json()

    def to_json(self):
        return {
            'id': self.id,
            'assignment_group_id': self.assignment_group_id,
            'assignment_id': self.assignment_id,
            'student_id': self.student_id,
            'assignment_name': self.assignment_name,
            'assignment_date': get_date_time_str(self.assignment_date),
            'submitted_date': get_date_time_str(self.submitted_date),
            'graded': self.graded,
            'score': int(self.score*10)/10,
            'points': int(self.points),
            'flow': int(self.flow*100)/100,
            'comments': list(map(lambda c: c.to_json(), self.comments)),
        }

    def __str__(self):
        return f'Submission({self.id}, {self.assignment_group_id}, {self.assignment_id}, {self.student_id}, {self.assignment_name}, {get_date_time_str(self.assignment_date)}, {get_date_time_str(self.submitted_date)}, {self.graded}, {self.score}, {self.points}, Comments: {len(self.comments)})'

    @staticmethod
    def from_dict(data_dict):
        new_submission = Submission(data_dict['id'], data_dict['assignment_group_id'], data_dict['assignment_id'], data_dict['student_id'], data_dict['assignment_name'],
                                    get_date_time_obj(data_dict['assignment_date']), get_date_time_obj(data_dict['submitted_date']), data_dict['graded'], data_dict['score'], data_dict['points'], data_dict['flow'])
        new_submission.comments = list(map(lambda c: Comment.from_dict(c), data_dict['comments']))
        return new_submission


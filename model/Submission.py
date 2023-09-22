from lib.config import get_date_time_obj, get_date_time_str
from model.Comment import Comment

class Submission:
    def __init__(self, submission_id, assignment_group_id, assignment_id, student_id, assignment_name, submitted_at, graded, score, points):
        self.id = submission_id
        self.assignment_group_id = assignment_group_id
        self.assignment_name = assignment_name
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.submitted_at = submitted_at
        self.graded = graded
        self.score = score
        self.points = points
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
            'submitted_at': get_date_time_str(self.submitted_at),
            'graded': self.graded,
            'score': self.score,
            'points': self.points,
            'comments': list(map(lambda c: c.to_json(), self.comments)),
        }

    def __str__(self):
        return f'Submission({self.id}, {self.assignment_group_id}, {self.assignment_id}, {self.student_id}, {self.assignment_name}, {get_date_time_str(self.submitted_at)}, {self.graded}, {self.score}, {self.points})'

    @staticmethod
    def from_dict(data_dict):
        new_submission = Submission(data_dict['id'], data_dict['assignment_group_id'], data_dict['assignment_id'], data_dict['student_id'], data_dict['assignment_name'], get_date_time_obj(data_dict['submitted_at']), data_dict['graded'], data_dict['score'], data_dict['points'])
        new_submission.comments = list(map(lambda c: Comment.from_dict(c), data_dict['comments']))
        return new_submission


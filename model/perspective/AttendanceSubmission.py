from lib.lib_date import get_date_time_obj, get_date_time_str
from model.Comment import Comment
from model.CriteriumScore import CriteriumScore


class AttendanceSubmission:
    def __init__(self, name, student_id, date, day, teacher, score, points, flow):
        self.name = name
        self.student_id = student_id
        self.date = date
        self.day = day
        self.teacher = teacher
        self.score = score
        self.points = points
        self.flow = flow

    def to_json(self):
        if self.score is None:
            self.score = 0.0
        return {
            'student_id': self.student_id,
            'name': self.name,
            'date': get_date_time_str(self.date),
            'day': self.day,
            'teacher': self.teacher,
            'score': round(self.score, 2),
            'points': int(self.points),
            'flow': round(self.flow, 2)
        }

    def __str__(self):
        return f'AttendanceSubmission({self.name}, {self.student_id}, {self.day} {get_date_time_str(self.date)}, {self.teacher}, {self.score})'

    @staticmethod
    def from_dict(data_dict):
        new = AttendanceSubmission(data_dict['name'], data_dict['student_id'],
                                    get_date_time_obj(data_dict['date']), data_dict['day'],
                                    data_dict['teacher'], data_dict['score'], data_dict['points'], data_dict['flow'])

        return new


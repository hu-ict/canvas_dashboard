from lib.lib_date import get_date_time_obj, get_date_time_str
from model.Comment import Comment
from model.CriteriumScore import CriteriumScore


class AttendanceSubmission:
    def __init__(self, name, student_id, date, day, teacher, grade, score, value, points, flow):
        self.name = name
        self.student_id = student_id
        self.date = date
        self.day = day
        self.teacher = teacher
        self.grade = grade
        self.score = score
        self.value = value
        self.points = points
        self.flow = flow

    def to_json(self):
        if self.flow is None:
            l_flow = None
        else:
            l_flow = round(self.flow, 3)
        if self.score is None:
            l_score = None
        else:
            l_score = round(self.score, 1)
        if self.value is None:
            l_value = None
        else:
            l_value = round(self.value, 1)
        return {
            'student_id': self.student_id,
            'name': self.name,
            'date': get_date_time_str(self.date),
            'day': self.day,
            'teacher': self.teacher,
            'grade': self.grade,
            'score': l_score,
            'value': l_value,
            'points': int(self.points),
            'flow': l_flow
        }

    def __str__(self):
        return f'AttendanceSubmission({self.name}, {self.student_id}, {self.day} {get_date_time_str(self.date)},' \
               f'{self.teacher}, {self.score})'

    @staticmethod
    def from_dict(data_dict):
        if "grade" in data_dict:
            new = AttendanceSubmission(data_dict['name'], data_dict['student_id'],
                                   get_date_time_obj(data_dict['date']), data_dict['day'],
                                   data_dict['teacher'], data_dict['grade'], data_dict['score'], None,
                                   data_dict['points'], data_dict['flow'])
        else:
            new = AttendanceSubmission(data_dict['name'], data_dict['student_id'],
                                   get_date_time_obj(data_dict['date']), data_dict['day'],
                                   data_dict['teacher'], None, data_dict['score'], None,
                                   data_dict['points'], data_dict['flow'])

        return new

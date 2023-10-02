from lib.config import get_date_time_obj, get_date_time_str
from model.Comment import Comment


class DataPoint:
    def __init__(self, a_name, a_date, a_graded, a_score, a_points):
        self.a_name = a_name
        self.date = a_date
        self.graded = a_graded
        self.score = a_score
        self.points = a_points
        self.comments = []

    def to_json(self):
        return {
            'name': self.name,
            'date': get_date_time_str(self.date),
            'graded': self.graded,
            'score': self.score,
            'points': self.points,
            'comments': list(map(lambda c: c.to_json(), self.comments)),
        }

    def __str__(self):
        return f'DataPoint({self.name}, {get_date_time_str(self.date)}, {self.graded}, {self.score}, {self.points}, Comments: {len(self.comments)})'

    @staticmethod
    def from_dict(data_dict):
        new = DataPoint(data_dict['name'], get_date_time_obj(data_dict['date']), data_dict['graded'], data_dict['score'], data_dict['points'])
        new.comments = list(map(lambda c: Comment.from_dict(c), data_dict['comments']))
        return new


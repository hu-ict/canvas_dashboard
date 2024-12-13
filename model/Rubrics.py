from model.Criterion import Criterion


class Rubrics:
    def __init__(self, name, points):
        self.name = name
        self.points = points
        self.criteria = []

    def to_json(self, scope, points):
        return {
            'name': self.name,
            'points': self.points,
            'criteria': list(map(lambda c: c.to_json([scope]), self.criteria)),
        }

    def __str__(self):
        line = f' Rubrics({self.name}, {self.points})\n'
        return line

    @staticmethod
    def from_dict(data_dict):
        new = Rubrics(data_dict['name'], data_dict['name'])
        new.criteria = list(map(lambda c: Criterion.from_dict(c), data_dict['criteria']))
        return new

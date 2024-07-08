from model.Assignment import Assignment


class AssignmentSeries:
    def __init__(self, assignment_name, tag, points):
        self.name = assignment_name
        self.tag = tag
        self.points = points
        self.assignments = []

    def __str__(self):
        return f'AssignmentImprovements({self.assignment_name}, {self.tag}, {self.points})'

    def to_json(self):
        return {
            'assignment_name': self.assignment_name,
            'tag': self.tag,
            'points': int(self.points),
            'assignments': list(map(lambda a: a.to_json(), self.assignments)),
        }

    @staticmethod
    def from_dict(data_dict):
        new = AssignmentSeries(data_dict['assignment_name'], data_dict['tag'], data_dict['points'])
        if 'assignments' in data_dict.keys():
            new.assignments = list(map(lambda a: Assignment.from_dict(a), data_dict['assignments']))
        return new

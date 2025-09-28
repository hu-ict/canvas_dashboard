from model.AssignmentSequence import AssignmentSequence
from model.Bandwidth import Bandwidth


class Perspective:
    def __init__(self, name, title, show_points, show_flow, total_points):
        self.name = name
        self.title = title
        self.show_points = show_points
        self.show_flow = show_flow
        self.total_points = total_points
        self.assignment_group_ids = []
        self.assignment_sequences = []
        self.bandwidth = Bandwidth()

    def to_json(self):
        dict_result = {
            'name': self.name,
            'title': self.title,
            'show_points': self.show_points,
            'show_flow': self.show_flow,
            'total_points': self.total_points,
            'assignment_group_ids': self.assignment_group_ids,
            'assignment_sequences': list(map(lambda a: a.to_json(), self.assignment_sequences)),
            'bandwidth': self.bandwidth.to_json()
        }
        return dict_result

    def __str__(self):
        return f'Perspective({self.name}, {self.title}, {self.assignment_group_ids}, {self.total_points})'

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        new = Perspective(data_dict['name'], data_dict['title'], data_dict['show_points'],
                          data_dict['show_flow'], data_dict['total_points'])
        if 'assignment_group_ids' in data_dict.keys():
            new.assignment_group_ids = data_dict['assignment_group_ids']
        if 'bandwidth' in data_dict.keys():
            new.bandwidth = Bandwidth.from_dict(data_dict['bandwidth'])
            # print("PERSP11 -", new.bandwidth)
        if 'assignment_sequences' in data_dict.keys():
            new.assignment_sequences = list(
                map(lambda a: AssignmentSequence.from_dict(a), data_dict['assignment_sequences']))
        return new

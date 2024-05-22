from model.perspective.Level import Level


class Perspective:
    def __init__(self, name, levels, show_points, show_flow):
        self.name = name
        self.levels = levels
        self.show_points = show_points
        self.show_flow = show_flow
        self.assignment_groups = []

    def to_json(self):
        dict_result = {
            'name': self.name,
            'levels': self.levels,
            'show_points': self.show_points,
            'show_flow': self.show_flow,
            'assignment_groups': self.assignment_groups
        }
        return dict_result

    def __str__(self):
        return f'Perspective({self.name}, {self.assignment_groups}, {self.levels})'

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        new = Perspective(data_dict['name'], data_dict['levels'], data_dict['show_points'], data_dict['show_flow'])
        if 'assignment_groups' in data_dict.keys():
            new.assignment_groups = data_dict['assignment_groups']
        return new

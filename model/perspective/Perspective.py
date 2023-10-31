from model.perspective.Level import Level
from model.perspective.Levels import Levels


class Perspective:
    def __init__(self, name, levels):
        self.name = name
        self.levels = levels
        self.assignment_groups = []


    def to_json(self):
        return {
            'name': self.name,
            'assignment_groups': self.assignment_groups,
            'levels': self.levels.to_json()
        }

    def __str__(self):
        return f'Perspective({self.name}, {self.assignment_groups}, {self.levels})'

    @staticmethod
    def from_dict(key, data_dict):
        # print("Perspective.from_dict", data_dict)
        new_levels = Levels.from_dict(data_dict['levels'])
        new = Perspective(key, new_levels)
        if 'assignment_groups' in data_dict.keys():
            new.assignment_groups = data_dict['assignment_groups']
        return new

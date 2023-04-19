from model.AssignmentGroup import AssignmentGroup


class Perspective:
    def __init__(self, name):
        self.name = name
        self.assigment_groups = []

    def to_json(self):
        return {
            'name': self.name,
            'assignment_groups': self.assignment_groups
        }

    def __str__(self):
        return f' Perspective({self.name}, {self.assignment_groups})\n'



    @staticmethod
    def from_dict(data_dict):
        new_perspective = Perspective(data_dict['name'])
        new_perspective.assignment_groups = data_dict['assignment_groups']
        return new_perspective

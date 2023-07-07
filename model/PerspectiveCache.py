from model.AssignmentGroup import AssignmentGroup


class PerspectiveCache:
    def __init__(self, name):
        self.name = name
        self.assignment_groups = []

    def to_json(self):
        return {
            'name': self.name,
            'assignment_groups': list(map(lambda g: g.to_json(), self.assignment_groups))
        }

    def __str__(self):
        line = f' PerspectiveCache({self.name})\n'
        for assignment_group in self.assignment_groups:
            line += " s " + str(assignment_group) + "\n"
        return line

    @staticmethod
    def from_dict(data_dict):
        new_perspective = PerspectiveCache(data_dict['name'])
        new_perspective.assignment_groups = list(map(lambda g: AssignmentGroup.from_dict(g), data_dict['assignment_groups']))
        return new_perspective

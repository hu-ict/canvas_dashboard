class AssignmentGroup:
    def __init__(self, id, name, scale, total_points, lower_points, upper_points):
        self.id = id
        self.name = name
        self.scale = scale
        self.total_points = total_points
        self.lower_points = lower_points
        self.upper_points = upper_points
        self.assignments = []


    def to_json(self, scope):
        if "assignment" in scope:
            return {
                'name': self.name,
                'id': self.id,
                'scale': self.scale,
                'total_points': self.total_points,
                'lower_points': self.lower_points,
                'upper_points': self.upper_points,
                'assignments': list(map(lambda a: a.to_json(), self.assignments)),
            }
        else:
            return {
                'name': self.name,
                'id': self.id,
                'scale': self.scale,
                'total_points': self.total_points,
                'lower_points': self.lower_points,
                'upper_points': self.upper_points,
        }

    def __str__(self):
        return f'AssigmentGroup({self.id}, {self.name}, {self.scale}, {self.total_points}, {self.lower_points}, {self.upper_points})'

    @staticmethod
    def from_dict(data_dict):
        return AssignmentGroup(data_dict['id'], data_dict['name'], data_dict['scale'], data_dict['total_points'], data_dict['lower_points'], data_dict['upper_points'])

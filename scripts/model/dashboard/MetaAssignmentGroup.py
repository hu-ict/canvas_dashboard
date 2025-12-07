class MetaAssignmentGroup:
    def __init__(self, name, groups, strategy, levels, marker, lower_c, upper_c, total_points, lower_points, upper_points):
        self.name = name
        self.groups = groups
        self.strategy = strategy
        self.levels = levels
        self.marker = marker
        self.lower_c = lower_c
        self.upper_c = upper_c
        self.total_points = total_points
        self.lower_points = lower_points
        self.upper_points = upper_points

    def to_json(self):
        json_string = {
            'name': self.name,
            'groups': self.groups,
            'strategy': self.strategy,
            'levels': self.levels,
            'marker': self.marker,
            'lower_c': self.lower_c,
            'upper_c': self.upper_c,
            'total_points': self.total_points,
            'lower_points': self.lower_points,
            'upper_points': self.upper_points

        }
        return json_string

    def __str__(self):
        line = f'MetaAssigmentGroup({self.name}, strategy={self.strategy}, points={self.total_points}, {self.lower_points}, {self.upper_points})'
        return line

    @staticmethod
    def from_dict(data_dict):
        new_assignment_group = MetaAssignmentGroup(data_dict['name'], data_dict['groups'], data_dict['strategy'], data_dict['levels'], data_dict['marker'], data_dict['lower_c'],
                                               data_dict['upper_c'], data_dict['total_points'],
                                               data_dict['lower_points'], data_dict['upper_points'])
        return new_assignment_group

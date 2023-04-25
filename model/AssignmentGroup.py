from model.Assignment import Assignment


class AssignmentGroup:
    def __init__(self, id, name, teachers, roles, total_points, lower_points, upper_points):
        self.id = id
        self.name = name
        self.teachers = teachers
        self.roles = roles
        self.total_points = total_points
        self.lower_points = lower_points
        self.upper_points = upper_points
        self.assignments = []

    def to_json(self, scope):
        if "assignment" in scope:
            return {
                'name': self.name,
                'id': self.id,
                'teachers': self.teachers,
                'roles': self.roles,
                'total_points': self.total_points,
                'lower_points': self.lower_points,
                'upper_points': self.upper_points,
                'assignments': list(map(lambda a: a.to_json(), self.assignments)),
            }
        else:
            return {
                'name': self.name,
                'id': self.id,
                'teachers': self.teachers,
                'roles': self.roles,
                'total_points': self.total_points,
                'lower_points': self.lower_points,
                'upper_points': self.upper_points,
        }

    def __str__(self):
        line =  f'AssigmentGroup({self.id}, {self.name}, {self.teachers}, {self.roles}, {self.total_points}, {self.lower_points}, {self.upper_points})\n'
        # for assignments in self.assignments:
        #     line += str(assignments)
        return line

    @staticmethod
    def from_dict(data_dict):
        new_assignment_group = AssignmentGroup(data_dict['id'], data_dict['name'], data_dict['teachers'], data_dict['roles'], data_dict['total_points'], data_dict['lower_points'], data_dict['upper_points'])
        new_assignment_group.assignments = list(map(lambda a: Assignment.from_dict(a), data_dict['assignments']))
        return new_assignment_group

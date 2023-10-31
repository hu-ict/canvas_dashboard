from model.Assignment import Assignment
from model.Bandwidth import Bandwidth


class AssignmentGroup:
    def __init__(self, id, name, teachers, role, total_points, lower_points, upper_points, bandwidth):
        self.id = id
        self.name = name
        self.teachers = teachers
        self.role = role
        self.total_points = total_points
        self.lower_points = lower_points
        self.upper_points = upper_points
        self.bandwidth = bandwidth
        self.assignments = []

    def to_json(self, scope):
        check = lambda x: self.bandwidth.to_json() if x is not None else None
        if "assignment" in scope:
            return {
                'name': self.name,
                'id': self.id,
                'teachers': self.teachers,
                'role': self.role,
                'total_points': self.total_points,
                'lower_points': self.lower_points,
                'upper_points': self.upper_points,
                'bandwidth': check(self.bandwidth),
                'assignments': list(map(lambda a: a.to_json(), self.assignments)),
            }
        else:
            return {
                'name': self.name,
                'id': self.id,
                'teachers': self.teachers,
                'role': self.role,
                'total_points': self.total_points,
                'lower_points': self.lower_points,
                'upper_points': self.upper_points,
                'bandwidth': check(self.bandwidth),
            }

    def find_assignment(self, a_assignment):
        for assignment in self.assignments:
            if assignment.id == a_assignment.id:
                return assignment
        return None

    def append_assignment(self, a_assignment):
        l_assignment = self.find_assignment(a_assignment)
        if l_assignment != None:
            # update
            if l_assignment.unlock_date > a_assignment.unlock_date:
                l_assignment.unlock_date = a_assignment.unlock_date
            if l_assignment.assignment_date < a_assignment.assignment_date:
                l_assignment.assignment_date = a_assignment.assignment_date
        else:
            # insert
            self.assignments.append(a_assignment)

    def __str__(self):
        line = f'AssigmentGroup({self.id}, {self.name}, {self.teachers}, {self.role}, {self.total_points}, {self.lower_points}, {self.upper_points})\n'
        for assignment in self.assignments:
            line += str(assignment)
        return line

    @staticmethod
    def from_dict(data_dict):
        if 'bandwidth' in data_dict.keys():
            new_bandwidth = Bandwidth.from_dict(data_dict['bandwidth'])
        else:
            new_bandwidth = None
        new_assignment_group = AssignmentGroup(data_dict['id'], data_dict['name'], data_dict['teachers'], data_dict['role'], data_dict['total_points'], data_dict['lower_points'], data_dict['upper_points'], new_bandwidth)
        new_assignment_group.assignments = list(map(lambda a: Assignment.from_dict(a), data_dict['assignments']))
        return new_assignment_group

from model.AssignmentSequence import AssignmentSequence
from model.Bandwidth import Bandwidth


class AssignmentGroup:
    def __init__(self, id, name, role, strategy, lower_c, upper_c, total_points, lower_points, upper_points, bandwidth):
        self.id = id
        self.name = name
        # self.teachers = teachers
        self.role = role
        self.strategy = strategy
        self.lower_c = lower_c
        self.upper_c = upper_c
        self.total_points = total_points
        self.lower_points = lower_points
        self.upper_points = upper_points
        self.bandwidth = bandwidth
        self.assignment_sequences = []

    def to_json(self, scope):
        check = lambda x: self.bandwidth.to_json() if x is not None else None
        json_string = {
            'name': self.name,
            'id': self.id,
            # 'teachers': self.teachers,
            'role': self.role,
            'strategy': self.strategy,
            'lower_c': self.lower_c,
            'upper_c': self.upper_c,
            'total_points': self.total_points,
            'lower_points': self.lower_points,
            'upper_points': self.upper_points,
            'bandwidth': check(self.bandwidth)
        }
        if "assignment" in scope:
            json_string['assignment_sequences'] = list(map(lambda a: a.to_json(), self.assignment_sequences))
        return json_string

    # def find_assignment(self, a_assignment):
    #     for assignment in self.assignments:
    #         if assignment.id == a_assignment.id:
    #             return assignment
    #     return None

    def get_assignment_sequence_by_assignment_id(self, assignment_id):
        for assignment_sequence in self.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                # print(submission_sequence.name, submission.assignment_name, submission.assignment_id, assignment_id)
                if int(assignment.assignment_id) == int(assignment_id):
                    return assignment_sequence
        return None

    def find_assignment_sequence_by_tag(self, a_tag):
        for assignment_sequence in self.assignment_sequences:
            if assignment_sequence.tag == a_tag:
                return assignment_sequence
        return None

    def append_assignment(self, a_tag, a_assignment):
        assignment_sequence = self.find_assignment_sequence_by_tag(a_tag)
        if assignment_sequence is None:
            assignment_sequence = AssignmentSequence(a_assignment.name, a_tag, a_assignment.grading_type,
                                                     a_assignment.points)
            self.assignment_sequences.append(assignment_sequence)
        assignment_sequence.assignments.append(a_assignment)

    def __str__(self):
        line = f'AssigmentGroup({self.id}, {self.name}, {self.role}, strategy={self.strategy}, points={self.total_points}, {self.lower_points}, {self.upper_points})\n'
        for assignment_sequence in self.assignment_sequences:
            line += str(assignment_sequence)
        return line

    @staticmethod
    def from_dict(data_dict):
        if 'bandwidth' in data_dict.keys():
            new_bandwidth = Bandwidth.from_dict(data_dict['bandwidth'])
        else:
            new_bandwidth = None
        new_assignment_group = AssignmentGroup(data_dict['id'], data_dict['name'],
                                               # data_dict['teachers'],
                                               data_dict['role'], data_dict['strategy'], data_dict['lower_c'],
                                               data_dict['upper_c'], data_dict['total_points'],
                                               data_dict['lower_points'], data_dict['upper_points'], new_bandwidth)
        if 'assignment_sequences' in data_dict.keys():
            new_assignment_group.assignment_sequences = list(
                map(lambda a: AssignmentSequence.from_dict(a), data_dict['assignment_sequences']))
        return new_assignment_group

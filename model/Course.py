from model.AssignmentGroup import AssignmentGroup
from model.Statistics import Statistics
from model.Student import *
from model.StudentGroup import StudentGroup

class Course:
    def __init__(self, pid, name, actual_date):
        self.students = {}
        self.name = name
        self.id = pid
        self.actual_date = actual_date
        self.statistics = Statistics(0, 0)
        self.assignmentGroups = []
        self.studentGroups = []

    def to_json(self, scope):
        return {
            'name': self.name,
            'id': self.id,
            'actual_date': self.actual_date,
            'statistics': self.statistics.to_json(),
            'assignment_groups': list(map(lambda a: a.to_json(["assignment"]), self.assignmentGroups)),
            'student_groups': list(map(lambda g: g.to_json([]), self.studentGroups)),
            'students': list(map(lambda s: s.to_json(["submission"]), self.students.values())),
        }

    def add_assignment(self, assignment):
        for self.assignmentGroup in self.assignmentGroups:
            if self.assignmentGroup.id == assignment.group_id:
                # self.assignmentGroup.total_points += assignment.points
                self.assignmentGroup.assignments.append(assignment)
                break

    @staticmethod
    def from_dict(data_dict):
        new_course = Course(data_dict['id'], data_dict['name'], data_dict['actual_date'])
        new_course.statistics = Statistics.from_dict(data_dict['statistics'])
        new_course.students = list(map(lambda s: Student.from_dict(s), data_dict['students']))
        new_course.assignmentGroups = list(map(lambda g: AssignmentGroup.from_dict(g), data_dict['assignments_group']))
        new_course.studentGroups = list(map(lambda g: StudentGroup.from_dict(g), data_dict['student_group']))
        return new_course

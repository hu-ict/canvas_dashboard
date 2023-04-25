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
        # self.assignmentGroups = []
        self.studentGroups = []

    def __str__(self):
        line = f'Course({self.id}, {self.actual_date}, {self.name}, {self.statistics}'
        # for a in self.assignmentGroups:
        #     line += " a "+str(a)
        for g in self.studentGroups:
            line += " g "+str(g)
        return line


    def to_json(self, scope):
        return {
            'name': self.name,
            'id': self.id,
            'actual_date': self.actual_date,
            'statistics': self.statistics.to_json(),
            # 'assignment_groups': list(map(lambda a: a.to_json(["assignment"]), self.assignmentGroups)),
            'student_groups': list(map(lambda g: g.to_json(['submission']), self.studentGroups)),
            # 'students': list(map(lambda s: s.to_json(["submission"]), self.students.values())),
        }

    def find_student(self, student_id):
        for group in self.studentGroups:
            for student in group.students:
                if student.id == student_id:
                    return student
        return None


    # def find_assignment(self, assigment_group_id, assignment_id):
    #     assignmentGroup = self.find_assignment_group(assigment_group_id)
    #     if not assignmentGroup:
    #         return None
    #     for assigment in assignmentGroup.assignments:
    #         if assigment.id == assignment_id:
    #             return assigment
    #     return None


    # def add_assignment(self, assignment):
    #     for self.assignmentGroup in self.assignmentGroups:
    #         if self.assignmentGroup.id == assignment.group_id:
    #             # self.assignmentGroup.total_points += assignment.points
    #             self.assignmentGroup.assignments.append(assignment)
    #             break

    @staticmethod
    def from_dict(data_dict):
        new_course = Course(data_dict['id'], data_dict['name'], data_dict['actual_date'])
        new_course.statistics = Statistics.from_dict(data_dict['statistics'])
        # new_course.students = list(map(lambda s: Student.from_dict(s), data_dict['students']))
        # new_course.assignmentGroups = list(map(lambda g: AssignmentGroup.from_dict(g), data_dict['assignments_groups']))
        new_course.studentGroups = list(map(lambda g: StudentGroup.from_dict(g), data_dict['student_groups']))
        return new_course

from datetime import datetime

from lib.config import get_date_time_str, get_date_time_obj
from model.StudentGroup import StudentGroup


class Course:
    def __init__(self, pid, name, actual_date):
        # self.students = {}
        self.name = name
        self.id = pid
        self.actual_date = actual_date
        self.student_groups = []

    def __str__(self):
        line = f'Course({self.id}, {get_date_time_str(self.actual_date)}, {self.name}'
        for g in self.student_groups:
            line += " g "+str(g)
        return line

    def to_json(self, scope):
        return {
            'name': self.name,
            'id': self.id,
            'actual_date': get_date_time_str(self.actual_date),
            'student_groups': list(map(lambda g: g.to_json(['submission']), self.student_groups)),
        }

    def find_student(self, student_id):
        for group in self.student_groups:
            for student in group.students:
                if student.id == student_id:
                    return student
        return None

    @staticmethod
    def from_dict(data_dict):
        new_course = Course(data_dict['id'], data_dict['name'], get_date_time_obj(data_dict['actual_date']))
        new_course.student_groups = list(map(lambda g: StudentGroup.from_dict(g), data_dict['student_groups']))
        return new_course

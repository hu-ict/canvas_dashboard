from datetime import datetime

from lib.lib_date import get_date_time_str, get_date_time_obj
from model.Student import Student
from model.StudentGroup import StudentGroup


class Result:
    def __init__(self, pid, name, actual_date, submission_count, not_graded_count):
        # self.students = {}
        self.id = pid
        self.name = name
        self.actual_date = get_date_time_obj(get_date_time_str(actual_date))
        self.submission_count = submission_count
        self.not_graded_count = not_graded_count

        self.students = []

    def __str__(self):
        line = f'Course({self.id}, {get_date_time_str(self.actual_date)}, {self.name}'
        for s in self.students:
            line += " s "+str(s)
        return line

    def to_json(self, scope):
        return {
            'id': self.id,
            'name': self.name,
            'actual_date': get_date_time_str(self.actual_date),
            'submission_count': self.submission_count,
            'not_graded_count': self.not_graded_count,
            'students': list(map(lambda g: g.to_json(['submissions']), self.students)),
        }

    def find_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    @staticmethod
    def from_dict(data_dict):
        new_course = Result(data_dict['id'], data_dict['name'], get_date_time_obj(data_dict['actual_date']), data_dict['submission_count'], data_dict['not_graded_count'])
        new_course.students = list(map(lambda g: Student.from_dict(g), data_dict['students']))
        return new_course

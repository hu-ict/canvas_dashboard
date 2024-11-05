from lib.lib_date import get_date_time_str, get_date_time_obj
from model.StudentResults import StudentResults


class Result:
    def __init__(self, course_id, name, actual_date, actual_day, submission_count, not_graded_count):
        # self.students = {}
        self.id = course_id
        self.name = name
        self.actual_date = get_date_time_obj(get_date_time_str(actual_date))
        self.actual_day = actual_day
        self.submission_count = submission_count
        self.not_graded_count = not_graded_count
        self.students = []

    def __str__(self):
        line = f'Course({self.id}, {get_date_time_str(self.actual_date)},  {self.actual_day}, {self.name}'
        for s in self.students:
            line += " s "+str(s)
        return line

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'actual_date': get_date_time_str(self.actual_date),
            'actual_day': self.actual_day,
            'submission_count': self.submission_count,
            'not_graded_count': self.not_graded_count,
            'students': list(map(lambda g: g.to_json(), self.students)),
        }

    def find_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    @staticmethod
    def from_dict(data_dict):
        new_course = Result(data_dict['id'], data_dict['name'], get_date_time_obj(data_dict['actual_date']), data_dict['actual_day'], data_dict['submission_count'], data_dict['not_graded_count'])
        new_course.students = list(map(lambda g: StudentResults.from_dict(g), data_dict['students']))
        return new_course

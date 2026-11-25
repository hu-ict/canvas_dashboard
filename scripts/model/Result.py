from scripts.lib.lib_date import get_date_time_str, get_date_time_obj
from scripts.model.StudentResults import StudentResults
from scripts.model.learning_outcome.SaturationLearningOutcome import SaturationLearningOutcome
from scripts.model.learning_outcome.SaturationStatistics import SaturationStatistics


class Result:
    def __init__(self, course_id, name, actual_date, actual_day, submission_count, not_graded_count):
        # self.students = {}
        self.id = course_id
        self.name = name
        self.actual_date = get_date_time_obj(get_date_time_str(actual_date))
        self.actual_day = actual_day
        self.submission_count = submission_count
        self.not_graded_count = not_graded_count
        self.saturation_learning_outcomes = []
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
            'saturation_learning_outcomes': list(map(lambda lo: lo.to_json(), self.saturation_learning_outcomes)),
            'students': list(map(lambda s: s.to_json(), self.students))
        }

    def find_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def get_learning_outcome(self, learning_outcome_id):
        for learning_outcome in self.saturation_learning_outcomes:
            if learning_outcome.id == learning_outcome_id:
                return learning_outcome
        return None

    def find_student_by_number(self, student_number):
        for student in self.students:
            if student.number == student_number:
                return student
        return None


    @staticmethod
    def from_dict(data_dict):
        new = Result(data_dict['id'], data_dict['name'], get_date_time_obj(data_dict['actual_date']), data_dict['actual_day'], data_dict['submission_count'], data_dict['not_graded_count'])
        new.students = list(map(lambda g: StudentResults.from_dict(g), data_dict['students']))
        new.saturation_learning_outcomes = list(map(lambda lo: SaturationLearningOutcome.from_dict(lo), data_dict['saturation_learning_outcomes']))
        return new

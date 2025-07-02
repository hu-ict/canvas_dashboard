from model.perspective.Level import Level
from model.perspective.Status import Status

STR_STATUS = "status"
STR_GRADES = "grades"


class LevelSerie:
    def __init__(self, a_name):
        self.name = a_name
        self.status = {}
        self.grades = {}

    def __str__(self):
        return f'LevelSerie({self.name}, {self.status}, {self.grades})'

    def to_json(self):
        dict_result = {STR_STATUS: {},
                       STR_GRADES: {}}
        for key in self.status:
            dict_result[STR_STATUS][key] = self.status[key].to_json()
        for key in self.grades:
            dict_result[STR_GRADES][key] = self.grades[key].to_json()
        return dict_result

    def get_status(self, status):
        return self.status[status]

    def get_grade_by_fraction(self, fraction):
        last_fraction = -0.05
        for grade in self.grades.values():
            # print("LS10", last_fraction, "<", fraction, "<=", grade.fraction, grade)
            if last_fraction < fraction <= grade.fraction:
                return grade
            last_fraction = grade.fraction
        return None

    @staticmethod
    def from_dict(data_dict, a_name):
        new = LevelSerie(a_name)
        for key in data_dict[STR_STATUS].keys():
            new.status[key] = Status.from_dict(data_dict[STR_STATUS][key])
        for key in data_dict[STR_GRADES].keys():
            new.grades[key] = Level.from_dict(data_dict[STR_GRADES][key])
        return new

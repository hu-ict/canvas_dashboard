from model.perspective.StudentPerspective import StudentPerspective


class StudentPerspectives:
    def __init__(self):
        self.perspectives = {}

    def to_json(self):
        dict_result = {}
        for key in self.perspectives:
            dict_result[key] = self.perspectives[key].to_json()
        return dict_result

    def __str__(self):
        line = f' StudentPerspectives({self.perspectives})'
        return line

    @staticmethod
    def from_dict(data_dict):
        # print(data_dict)
        new = StudentPerspectives()
        for key in data_dict.keys():
            new.perspectives[key] = StudentPerspective.from_dict(data_dict[key])
        return new

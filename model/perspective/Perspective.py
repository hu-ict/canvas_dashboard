from model.perspective.Level import Level


class Perspective:
    def __init__(self, name):
        self.name = name
        self.levels = {}
        self.assignment_groups = []


    def to_json(self):
        dict_result = {
            'name': self.name,
            'assignment_groups': self.assignment_groups,
            'levels': {}
        }
        for key in self.levels:
            dict_result['levels'][key] = self.levels[key].to_json()
        return dict_result

    def __str__(self):
        return f'Perspective({self.name}, {self.assignment_groups}, {self.levels})'

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        new = Perspective(data_dict['name'])
        if 'assignment_groups' in data_dict.keys():
            new.assignment_groups = data_dict['assignment_groups']
        if 'levels' in data_dict.keys():
            for key in data_dict['levels'].keys():
                new.levels[key] = Level.from_dict(data_dict['levels'][key])

        return new

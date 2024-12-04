class Action:
    def __init__(self, name, run):
        self.name = name
        self.run = run

    def __str__(self):
        return f'  Action({self.name}, {self.run})'

    def to_json(self):
        dict_result = {
            'name': self.name,
            'run': self.run
        }
        return dict_result

    @staticmethod
    def from_dict(key, data_dict):
        # print(data_dict)
        new = Action(data_dict['name'], data_dict['run'])
        return new

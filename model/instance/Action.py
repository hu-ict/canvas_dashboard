class Action:
    def __init__(self, name, run):
        self.name = name
        self.run = run

    def __str__(self):
        return f'  Action({self.name}, {self.run})'


    @staticmethod
    def from_dict(key, data_dict):
        # print(data_dict)
        new = Action(data_dict['name'], data_dict['run'])
        return new

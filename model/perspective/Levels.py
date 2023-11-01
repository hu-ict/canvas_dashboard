from model.perspective.Level import Level


class Levels:
    def __init__(self):
        self.levels = {}

    def to_json(self):
        dict_result = {}
        for key in self.levels:
            dict_result[key] = self.levels[key].to_json()
        return dict_result


    @staticmethod
    def from_dict(data_dict):
        new = Levels()
        for key in data_dict.keys():
            new.levels[key] = Level.from_dict(data_dict[key])
        return new

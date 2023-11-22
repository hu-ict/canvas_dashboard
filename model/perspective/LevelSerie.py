from model.perspective.Level import Level


class LevelSerie:
    def __init__(self, a_name):
        self.levels = {}
        self.name = a_name

    def to_json(self):
        dict_result = {}
        for key in self.levels:
            dict_result[key] = self.levels[key].to_json()
        return dict_result

    @staticmethod
    def from_dict(data_dict, a_name):
        new = LevelSerie(a_name)
        for key in data_dict.keys():
            new.levels[key] = Level.from_dict(data_dict[key])
        return new

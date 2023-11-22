from model.perspective.LevelSerie import LevelSerie


class LevelSeries:
    def __init__(self):
        self.level_series = {}

    def to_json(self):
        dict_result = {}
        for key in self.level_series:
            dict_result[key] = self.level_series[key].to_json()
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        new = LevelSeries()
        for key in data_dict.keys():
            new.level_series[key] = LevelSerie.from_dict(data_dict[key], key)
        return new

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

    def get_level_by_fraction(self, fraction):
        last_fraction = 0.0
        for level in self.levels.keys():
            if self.levels[level].fraction:
                if last_fraction < fraction <= self.levels[level].fraction:
                    # print(last_fraction, "<", fraction, "<", self.levels[level].fraction, level)
                    return level
                last_fraction = self.levels[level].fraction
        return 0

    @staticmethod
    def from_dict(data_dict, a_name):
        new = LevelSerie(a_name)
        for key in data_dict.keys():
            new.levels[key] = Level.from_dict(data_dict[key])
        return new

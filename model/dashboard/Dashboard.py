from model.dashboard.LevelSerieCollection import LevelSerieCollection
from model.dashboard.Subplot import Subplot


class Dashboard:
    def __init__(self, dashboard_tabs, student_tabs, subplot, level_serie_collection):
        self.dashboard_tabs = dashboard_tabs
        self.student_tabs = student_tabs
        self.subplot = subplot
        self.level_serie_collection = level_serie_collection


    def to_json(self):
        dict_result = {"dashboard_tabs": self.dashboard_tabs, "student_tabs": self.student_tabs,
                       "subplot": self.subplot.to_json(),
                       "level_serie_collection": self.level_serie_collection.to_json()}
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        new = Dashboard(data_dict["dashboard_tabs"], data_dict["student_tabs"], Subplot.from_dict(data_dict["subplot"]), LevelSerieCollection.from_dict(data_dict["level_serie_collection"]))
        return new

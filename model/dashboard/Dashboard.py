from model.Role import Role
from model.dashboard.LevelSerieCollection import LevelSerieCollection
from model.dashboard.MetaAssignmentGroup import MetaAssignmentGroup
from model.dashboard.Subplot import Subplot
from model.learning_outcome.LearningOutcome import LearningOutcome
from model.dashboard.MetaPerspective import MetaPerspective


class Dashboard:
    def __init__(self, dashboard_tabs, student_tabs, subplot, project_group_name, guild_group_name, feedback_colors, level_serie_collection):
        self.dashboard_tabs = dashboard_tabs
        self.student_tabs = student_tabs
        self.subplot = subplot
        self.project_group_name = project_group_name
        self.guild_group_name = guild_group_name
        self.feedback_colors = feedback_colors
        self.level_serie_collection = level_serie_collection
        self.roles = []
        self.learning_outcomes = []
        self.perspectives = []
        self.assignment_groups = []

    def get_assignment_group_by_name(self, assignment_group_name):
        for assignment_group in self.assignment_groups:
            if assignment_group.name == assignment_group_name:
                return assignment_group
        return None

    def to_json(self):
        dict_result = {"dashboard_tabs": self.dashboard_tabs, "student_tabs": self.student_tabs,
                       "subplot": self.subplot.to_json(), "project_group_name": self.project_group_name, "guild_group_name": self.guild_group_name, "feedback_colors": self.feedback_colors,
                       "level_serie_collection": self.level_serie_collection.to_json()}
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        new = Dashboard(data_dict["dashboard_tabs"], data_dict["student_tabs"], Subplot.from_dict(data_dict["subplot"]),
                        data_dict["project_group_name"], data_dict["guild_group_name"], data_dict["feedback_colors"],
                        LevelSerieCollection.from_dict(data_dict["level_serie_collection"]))
        if "perspectives" in data_dict:
            new.perspectives = list(map(lambda p: MetaPerspective.from_dict(p), data_dict['perspectives']))
        if "assignment_groups" in data_dict:
            new.assignment_groups = list(map(lambda a: MetaAssignmentGroup.from_dict(a), data_dict['assignment_groups']))
        if 'learning_outcomes' in data_dict.keys() and data_dict['learning_outcomes'] is not None:
            new.learning_outcomes = list(map(lambda l: LearningOutcome.from_dict(l), data_dict['learning_outcomes']))
        if "roles" in data_dict.keys() and data_dict['roles'] is not None:
            new.roles = list(map(lambda r: Role.from_dict(r), data_dict['roles']))
        return new
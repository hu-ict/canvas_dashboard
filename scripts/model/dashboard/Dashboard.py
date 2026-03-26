from scripts.model.Role import Role
from scripts.model.dashboard.Groups import Groups
from scripts.model.dashboard.LevelSerieCollection import LevelSerieCollection
from scripts.model.dashboard.MetaAssignmentGroup import MetaAssignmentGroup
from scripts.model.dashboard.Subplot import Subplot
from scripts.model.learning_outcome.LearningOutcome import LearningOutcome
from scripts.model.dashboard.MetaPerspective import MetaPerspective
from scripts.model.moment.MetaGradeMoments import MetaGradeMoments
from scripts.model.moment.MetaLevelMoments import MetaLevelMoments


class Dashboard:
    def __init__(self, dashboard_tabs, student_tabs, subplot, feedback_colors, level_serie_collection):
        self.dashboard_tabs = dashboard_tabs
        self.student_tabs = student_tabs
        self.subplot = subplot
        self.feedback_colors = feedback_colors
        self.level_serie_collection = level_serie_collection
        self.groups_1 = None
        self.groups_2 = None
        self.roles = []
        self.learning_outcomes = []
        self.level_moments = None
        self.grade_moments = None
        self.perspectives = []
        self.assignment_groups = []

    def get_assignment_group_by_name(self, assignment_group_name):
        for assignment_group in self.assignment_groups:
            print("DSHB11 -", assignment_group.name, assignment_group_name)
            if assignment_group.name == assignment_group_name:
                return assignment_group
        # print("DSHB11 -", assignment_group.name, assignment_group_name)
        return None

    def to_json(self):
        dict_result = {"dashboard_tabs": self.dashboard_tabs,
                       "groups_1": self.groups_1.to_json(), "groups_2": self.groups_2.to_json(),
                       "perspectives": self.perspectives,
                       "level_moments": self.level_moments, "grade_moments": self.grade_moments,
                       "assignment_groups": list(map(lambda a: a.to_json(), self.assignment_groups)),
                       "roles": list(map(lambda r: r.to_json(), self.roles)),
                       "student_tabs": self.student_tabs,
                       "learning_outcomes": self.learning_outcomes,
                       "subplot": self.subplot.to_json(), "feedback_colors": self.feedback_colors,
                       "level_serie_collection": self.level_serie_collection.to_json()}
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        # print("DAS04 -", data_dict)
        new = Dashboard(data_dict["dashboard_tabs"], data_dict["student_tabs"], Subplot.from_dict(data_dict["subplot"]),
                        data_dict["feedback_colors"], LevelSerieCollection.from_dict(data_dict["level_serie_collection"]))
        if "groups_1" in data_dict:
            # print("DAS05 -", data_dict["level_moments"])
            new.groups_1 = Groups.from_dict(data_dict['groups_1'])
        if "groups_2" in data_dict:
            # print("DAS05 -", data_dict["level_moments"])
            new.groups_2 = Groups.from_dict(data_dict['groups_2'])
        if "level_moments" in data_dict:
            # print("DAS05 -", data_dict["level_moments"])
            new.level_moments = MetaLevelMoments.from_dict(data_dict['level_moments'])
        if "grade_moments" in data_dict:
            # print("DAS05 -", len(data_dict["perspectives"]))
            new.grade_moments = MetaGradeMoments.from_dict(data_dict['grade_moments'])
        if "perspectives" in data_dict:
            # print("DAS05 -", len(data_dict["perspectives"]))
            new.perspectives = list(map(lambda p: MetaPerspective.from_dict(p), data_dict['perspectives']))
        if "assignment_groups" in data_dict:
            new.assignment_groups = list(map(lambda a: MetaAssignmentGroup.from_dict(a), data_dict['assignment_groups']))
        if 'learning_outcomes' in data_dict.keys() and data_dict['learning_outcomes'] is not None:
            new.learning_outcomes = list(map(lambda l: LearningOutcome.from_dict(l), data_dict['learning_outcomes']))
        if "roles" in data_dict.keys() and data_dict['roles'] is not None:
            new.roles = list(map(lambda r: Role.from_dict(r), data_dict['roles']))
        return new
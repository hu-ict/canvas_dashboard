from scripts.model.environment.Action import Action


class Workflow:
    def __init__(self, name):
        self.name = name
        self.actions = []

    def to_json(self):
        return {'name': self.name, 'actions': list(map(lambda a: a.to_json(), self.actions))}

    def __str__(self):
        return f'Workflow({self.name})'

    def get_action_by_name(self, action_name):
        for action in self.actions:
            if action.name == action_name:
                return action
        return None

    def new_instance(self):
        self.actions.append(Action('course_create_event',
                                                    ["generate_course.py", "generate_students.py",
                                                     "generate_results.py", "generate_dashboard.py",
                                                     "generate_plotly.py", "generate_portfolio.py",
                                                     "publish_dashboard.py"]))
        self.actions.append(Action('course_update_event',
                                                    ["generate_course.py", "generate_students.py",
                                                     "generate_results.py", "generate_dashboard.py",
                                                     "generate_plotly.py", "generate_portfolio.py",
                                                     "publish_dashboard.py"]))
        self.actions.append(Action('results_create_event',
                                                     ["generate_results.py", "generate_dashboard.py",
                                                      "generate_plotly.py", "generate_portfolio.py",
                                                      "publish_dashboard.py"]))
        self.actions.append(Action('results_update_event',
                                                     ["generate_submissions.py", "generate_dashboard.py",
                                                      "generate_plotly.py", "generate_portfolio.py",
                                                      "publish_dashboard.py"]))

    @staticmethod
    def from_dict(data_dict):
        new = Workflow(data_dict["name"])
        new.actions = list(map(lambda c: Action.from_dict(c), data_dict['actions']))
        return new

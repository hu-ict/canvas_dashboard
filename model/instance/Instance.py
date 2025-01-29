from model.instance.Action import Action


class Instance:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.listen = {}

    def new_instance(self):
        self.listen['course_create_event'] = Action('course_create_event',
                                                    ["generate_course.py", "generate_students.py",
                                                     "generate_results.py", "generate_dashboard.py",
                                                     "generate_plotly.py", "publish_dashboard.py"])
        self.listen['course_update_event'] = Action('course_update_event',
                                                    ["generate_course.py", "generate_students.py",
                                                     "generate_results.py", "generate_dashboard.py",
                                                     "generate_plotly.py", "publish_dashboard.py"])
        self.listen['results_create_event'] = Action('results_create_event',
                                                     ["generate_results.py", "generate_dashboard.py",
                                                      "generate_plotly.py", "publish_dashboard.py"])
        self.listen['results_update_event'] = Action('results_update_event',
                                                     ["generate_submissions.py", "generate_dashboard.py",
                                                      "generate_plotly.py", "publish_dashboard.py"])

    def to_json(self):
        dict_result = {
            'name': self.name,
            'category': self.category,
            'listen': {}
        }
        for key in self.listen:
            dict_result['listen'][key] = self.listen[key].to_json()
        return dict_result

    def __str__(self):
        line = f' Instance({self.name}, {self.category})\n'
        for key in self.listen.keys():
            line += f'{self.listen[key]}\n'
        return line

    def is_instance_of(self, category):
        return self.category == category

    def get_project_path(self):
        return ".//courses//" + self.name + "//"

    def get_test_path(self):
        return self.get_project_path() + "test//"

    def get_temp_path(self):
        return self.get_project_path() + "temp//"

    def get_template_path(self):
        return ".//templates//"

    def get_student_path(self):
        return self.get_project_path() + "dashboard_" + self.name + "//" + self.name + "//students//"

    def get_html_path(self):
        return self.get_project_path() + "dashboard_" + self.name + "//" + self.name + "//general//"

    def get_html_root_path(self):
        return self.get_project_path() + "dashboard_" + self.name + "//"

    def get_start_file_name(self):
        return self.get_project_path() + "start_" + self.name + ".json"

    def get_config_file_name(self):
        return self.get_project_path() + "config_"+self.name+".json"

    def get_course_file_name(self):
        return self.get_project_path() + "course_"+self.name+".json"

    def get_result_file_name(self):
        return self.get_project_path() + "result_"+self.name+".json"

    def get_progress_file_name(self):
        return self.get_project_path() + "progress_"+self.name+".json"

    def get_workload_file_name(self):
        return self.get_project_path() + "workload_"+self.name+".json"

    def from_dict(key, data_dict):
        # print(data_dict)
        new = Instance(data_dict["name"], data_dict["category"])
        for key in data_dict["listen"].keys():
            new.listen[key] = Action.from_dict(key, data_dict["listen"][key])
        return new

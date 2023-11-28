from model.CourseCategory import CourseCatergory


class CourseInstances:
    def __init__(self, current_instance):
        self.current_instance = current_instance
        self.course_categories = {}

    def to_json(self):
        dict_result = {
            'current_instance': self.current_instance,
            'course_categories': {}
        }
        for key in self.course_categories:
            dict_result['course_categories'][key] = self.course_categories[key].to_json()
        return dict_result

    def __str__(self):
        line = f'CourseInstances({self.current_instance})\n'
        for key in self.course_categories.keys():
            line += f'({self.course_categories[key]})\n'
        return line

    def get_project_path(self):
        return ".//courses//" + self.current_instance + "//"

    def get_plot_path(self):
        return self.get_project_path() + "dashboard_" + self.current_instance + "//plotly//"

    def get_html_path(self):
        return self.get_project_path() +"dashboard_" + self.current_instance + "//"

    def get_start_file_name(self):
        return self.get_project_path() + "start_" + self.current_instance + ".json"

    def is_instance_of(self, category):
        return self.current_instance in self.course_categories[category].course_instances

    @staticmethod
    def from_dict(data_dict):
        # print(data_dict)
        new = CourseInstances(data_dict["current_instance"])
        for key in data_dict["course_categories"].keys():
            # print(key, data_dict["course_categories"][key])
            new.course_categories[key] = CourseCatergory.from_dict(key, data_dict["course_categories"][key])
        return new
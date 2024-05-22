from model.instance.Event import Event
from model.instance.Instance import Instance
from model.instance.CourseCategory import CourseCatergory

class CourseInstances:
    def __init__(self, current_instance):
        self.current_instance = current_instance
        self.course_categories = {}
        self.instances = {}
        self.events = {}

    def to_json(self):
        dict_result = {
            'current_instance': self.current_instance,
            'course_categories': {},
            'instances': {},
            'events': {}
        }
        for key in self.course_categories:
            dict_result['course_categories'][key] = self.course_categories[key].to_json()
        for key in self.instances:
            dict_result['instances'][key] = self.instances[key].to_json()
        for key in self.events:
            dict_result['events'][key] = self.events[key].to_json()
        return dict_result

    def __str__(self):
        line = f'CourseInstances({self.current_instance})\n'
        for key in self.course_categories.keys():
            line += f'{self.course_categories[key]}'
        for key in self.instances.keys():
            line += f'{self.instances[key]}'
        for key in self.events.keys():
            line += f'{self.events[key]}'
        return line

    def get_project_path(self):
        return ".//courses//" + self.current_instance + "//"

    def get_test_path(self):
        return self.get_project_path() + "test//"

    def get_plot_path(self):
        return self.get_project_path() + "dashboard_" + self.current_instance + "//plotly//"

    def get_html_path(self):
        return self.get_project_path() +"dashboard_" + self.current_instance + "//"

    def get_start_file_name(self):
        return self.get_project_path() + "start_" + self.current_instance + ".json"

    def get_category(self, instance_name):
        for category in self.course_categories.values():
            for instance in category.course_instances:
                if instance_name == instance:
                    return category.category
        return None

    def is_instance_of(self, category):
        for key in self.instances.keys():
            if self.current_instance == key:
                if self.instances[key].category == category:
                    return True
        return False

    def is_instance(self, instance_name):
        for key in self.course_categories.keys():
            if instance_name in self.course_categories[key].course_instances:
                return True
        return False

    @staticmethod
    def from_dict(data_dict):
        # print(data_dict)
        new = CourseInstances(data_dict["current_instance"])
        for key in data_dict["course_categories"].keys():
            # print(key, data_dict["course_categories"][key])
            new.course_categories[key] = CourseCatergory.from_dict(key, data_dict["course_categories"][key])
        for key in data_dict["instances"].keys():
            new.instances[key] = Instance.from_dict(key, data_dict["instances"][key])
        for key in data_dict["events"].keys():
            new.events[key] = Event.from_dict(key, data_dict["events"][key])
        return new

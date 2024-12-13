from model.instance.Event import Event
from model.instance.Instance import Instance
from model.instance.CourseCategory import CourseCategory


class CourseInstances:
    def __init__(self, current_instance):
        self.current_instance = current_instance
        self.course_categories = {}
        self.instances = {}
        self.events = {}

    def new_environment(self):
        self.course_categories['inno_courses'] = CourseCategory('inno_courses', [])
        self.course_categories['prop_courses'] = CourseCategory('prop_courses', [])
        self.course_categories['other_courses'] = CourseCategory('other_courses', [])
        self.events['course_create_event'] = Event('course_create_event', 'TIME')
        self.events['course_update_event'] = Event('course_update_event', 'TIME')
        self.events['results_create_event'] = Event('results_create_event', 'TIME')
        self.events['results_update_event'] = Event('results_update_event', 'TIME')

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

    @staticmethod
    def get_project_path(instance):
        return ".//courses//" + instance + "//"

    def get_test_path(self):
        return CourseInstances.get_project_path(self.current_instance) + "test//"

    def get_student_path(self):
        return CourseInstances.get_project_path(self.current_instance) + "dashboard_" + self.current_instance + "//students//"

    def get_html_path(self):
        return CourseInstances.get_project_path(self.current_instance) + "dashboard_" + self.current_instance + "//general//"

    def get_html_root_path(self):
        return CourseInstances.get_project_path(self.current_instance) + "dashboard_" + self.current_instance + "//"

    def get_start_file_name(self):
        return CourseInstances.get_project_path(self.current_instance) + "start_" + self.current_instance + ".json"

    @staticmethod
    def get_template_path():
        return ".//templates//"

    @staticmethod
    def get_config_file_name(instance_name):
        return CourseInstances.get_project_path(instance_name) + "config_" + instance_name + ".json"

    @staticmethod
    def get_course_file_name(instance_name):
        return CourseInstances.get_project_path(instance_name) + "course_" + instance_name + ".json"

    @staticmethod
    def get_result_file_name(instance_name):
        return CourseInstances.get_project_path(instance_name) + "result_" + instance_name + ".json"

    @staticmethod
    def get_progress_file_name(instance_name):
        return CourseInstances.get_project_path(instance_name) + "progress_" + instance_name + ".json"

    @staticmethod
    def get_workload_file_name(instance_name):
        return CourseInstances.get_project_path(instance_name) + "workload_" + instance_name + ".json"

    def get_category(self, instance_name):
        for category in self.course_categories.values():
            for instance in category.course_instances:
                if instance_name == instance:
                    return category.category
        return None

    def get_instance_by_name(self, instance_name):
        for instance in self.instances.values():
            if instance.name == instance_name:
                return instance
        return None

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
            new.course_categories[key] = CourseCategory.from_dict(key, data_dict["course_categories"][key])
        for key in data_dict["instances"].keys():
            new.instances[key] = Instance.from_dict(key, data_dict["instances"][key])
        for key in data_dict["events"].keys():
            new.events[key] = Event.from_dict(key, data_dict["events"][key])
        return new

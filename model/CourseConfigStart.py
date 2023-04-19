from model.Perspective import Perspective


class CourseConfigStart:
    def __init__(self, course_id, projects_groep_name, config_file_name, course_file_name, api_key):
        self.course_id = course_id
        self.api_key = api_key
        self.perspectives = []
        self.projects_groep_name = projects_groep_name
        self.config_file_name = config_file_name
        self.course_file_name = course_file_name

    def __str__(self):
        return f'CourseConfigStart({self.course_id}, {self.projects_groep_name}, {self.config_file_name}, {self.course_file_name}, {self.api_key})\n'

    @staticmethod
    def from_dict(data_dict):
        new_course_config_start = CourseConfigStart(data_dict['course_id'], data_dict['projects_groep_name'], data_dict['config_file_name'], data_dict['course_file_name'], data_dict['api_key'])
        new_course_config_start.perspectives = list(map(lambda p: Perspective.from_dict(p), data_dict['perspectives']))
        return new_course_config_start


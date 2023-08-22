from lib.config import get_date_time_obj
from model.Perspective import Perspective
from model.Role import Role


class CourseConfigStart:
    def __init__(self, course_id, projects_groep_name, slb_groep_name, peil_perspective, start_date, end_date, config_file_name, course_file_name, results_file_name, api_key):
        self.course_id = course_id
        self.api_key = api_key
        self.perspectives = []
        self.roles = []
        self.projects_groep_name = projects_groep_name
        self.slb_groep_name = slb_groep_name
        self.peil_perspective = peil_perspective
        self.start_date = start_date
        self.end_date = end_date
        self.config_file_name = config_file_name
        self.course_file_name = course_file_name
        self.results_file_name = results_file_name

    def __str__(self):
        return f'CourseConfigStart({self.course_id}, {self.projects_groep_name}, {self.slb_groep_name}, {self.peil_perspective},  {self.start_date}, {self.end_date}, {self.config_file_name}, {self.course_file_name}, {self.results_file_name}, {self.api_key})\n'

    @staticmethod
    def from_dict(data_dict):
        new_course_config_start = CourseConfigStart(data_dict['course_id'],
                                                    data_dict['projects_groep_name'],
                                                    data_dict['slb_groep_name'],
                                                    data_dict['peil_perspective'],
                                                    get_date_time_obj(data_dict['start_date']),
                                                    get_date_time_obj(data_dict['end_date']),
                                                    data_dict['config_file_name'], data_dict['course_file_name'],
                                                    data_dict['results_file_name'], data_dict['api_key'])
        new_course_config_start.perspectives = list(map(lambda p: Perspective.from_dict(p), data_dict['perspectives']))
        new_course_config_start.roles = list(map(lambda r: Role.from_dict(r), data_dict['roles']))
        return new_course_config_start


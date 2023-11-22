from lib.lib_date import get_date_time_obj, get_date_time_str
from model.Role import Role
from model.perspective.Level import Level
from model.perspective.Perspective import Perspective
from model.perspective.Perspectives import Perspectives


class CourseConfigStart:
    def __init__(self, course_id, projects_groep_name, slb_groep_name, progress_perspective, start_date, end_date, config_file_name, course_file_name, results_file_name, progress_file_name, api_key, a_grade_levels):
        self.course_id = course_id
        self.api_key = api_key
        self.perspectives = {}
        self.roles = []
        self.grade_levels = a_grade_levels
        self.projects_groep_name = projects_groep_name
        self.slb_groep_name = slb_groep_name
        self.progress_perspective = progress_perspective
        self.start_date = get_date_time_obj(get_date_time_str(start_date))
        self.end_date = end_date
        self.config_file_name = config_file_name
        self.course_file_name = course_file_name
        self.results_file_name = results_file_name
        self.progress_file_name = progress_file_name

    def __str__(self):
        return f'CourseConfigStart({self.course_id}, {self.projects_groep_name}, {self.slb_groep_name}, {self.progress_perspective},  {self.start_date}, {self.end_date}, {self.config_file_name}, {self.course_file_name}, {self.results_file_name}, {self.progress_file_name}, {self.api_key})\n'

    @staticmethod
    def from_dict(data_dict):
        new = CourseConfigStart(data_dict['course_id'],
                                data_dict['projects_groep_name'],
                                data_dict['slb_groep_name'],
                                data_dict['progress_perspective'],
                                get_date_time_obj(data_dict['start_date']),
                                get_date_time_obj(data_dict['end_date']),
                                data_dict['config_file_name'], data_dict['course_file_name'],
                                data_dict['results_file_name'], data_dict['progress_file_name'],
                                data_dict['api_key'],
                                data_dict['grade_levels'])
        if data_dict['perspectives']:
            for key in data_dict['perspectives'].keys():
                new.perspectives[key] = Perspective.from_dict(data_dict['perspectives'][key])
        new.roles = list(map(lambda r: Role.from_dict(r), data_dict['roles']))
        return new


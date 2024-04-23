from lib.lib_date import get_date_time_obj, get_date_time_str
from model.Role import Role
from model.perspective.Perspective import Perspective


class Start:
    def __init__(self, canvas_course_id, projects_groep_name, slb_groep_name,
                 progress, attendance_perspective, start_date,
                 end_date, template_path, target_path, target_slb_path, config_file_name, course_file_name,
                 results_file_name, progress_file_name, workload_file_name, attendance_report,
                 api_key, a_grade_levels):
        self.canvas_course_id = canvas_course_id
        self.api_key = api_key
        self.progress = {}
        self.perspectives = {}
        self.roles = []
        self.grade_levels = a_grade_levels
        self.projects_groep_name = projects_groep_name
        self.slb_groep_name = slb_groep_name
        self.attendance_perspective = attendance_perspective
        self.start_date = start_date
        self.end_date = end_date
        self.template_path = template_path
        self.target_path = target_path
        self.target_slb_path = target_slb_path
        self.config_file_name = config_file_name
        self.course_file_name = course_file_name
        self.results_file_name = results_file_name
        self.progress_file_name = progress_file_name
        self.workload_file_name = workload_file_name
        self.attendance_report = attendance_report

    def __str__(self):
        return f'Start({self.canvas_course_id}, {self.projects_groep_name}, {self.slb_groep_name}, {self.progress}, {self.attendance_perspective},  {self.start_date}, {self.end_date}, {self.config_file_name}, {self.course_file_name}, {self.results_file_name}, {self.progress_file_name}, {self.api_key})\n'

    def to_json(self, scope):
        dict_result = {
            'api_key': self.api_key,
            'canvas_course_id': self.canvas_course_id,
            'grade_levels': self.grade_levels,
            'projects_groep_name': self.projects_groep_name,
            "slb_groep_name": self.slb_groep_name,
            'start_date': get_date_time_str(self.start_date),
            'end_date': get_date_time_str(self.end_date),
            'attendance_perspective': self.attendance_perspective,
            'template_path': self.template_path,
            'target_path': self.target_path,
            'target_slb_path': self.target_slb_path,
            'config_file_name': self.config_file_name,
            'course_file_name': self.course_file_name,
            'results_file_name': self.results_file_name,
            'progress_file_name': self.progress_file_name,
            'workload_file_name': self.workload_file_name,
            'attendance_report': self.attendance_report,
            'progress': self.progress.to_json(),
            'perspectives': {},
            'roles': []
        }
        for key in self.perspectives:
            dict_result['perspectives'][key] = self.perspectives[key].to_json()
        for role in self.roles:
            dict_result['roles'].append(role.to_json([]))
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        new = Start(data_dict['canvas_course_id'],
                    data_dict['projects_groep_name'],
                    data_dict['slb_groep_name'],
                    data_dict['progress'],
                    data_dict['attendance_perspective'],
                    get_date_time_obj(data_dict['start_date']),
                    get_date_time_obj(data_dict['end_date']),
                    data_dict['template_path'], data_dict['target_path'], data_dict['target_slb_path'],
                    data_dict['config_file_name'], data_dict['course_file_name'],
                    data_dict['results_file_name'], data_dict['progress_file_name'], data_dict['workload_file_name'],
                    data_dict['attendance_report'],
                    data_dict['api_key'],
                    data_dict['grade_levels'])
        if data_dict['progress']:
            new.progress = Perspective.from_dict(data_dict['progress'])
        if data_dict['perspectives']:
            for key in data_dict['perspectives'].keys():
                new.perspectives[key] = Perspective.from_dict(data_dict['perspectives'][key])
        new.roles = list(map(lambda r: Role.from_dict(r), data_dict['roles']))
        return new

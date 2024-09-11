from lib.lib_date import get_date_time_obj, get_date_time_str
from model.Role import Role
from model.perspective.Attendance import Attendance
from model.perspective.LevelMoments import LevelMoments
from model.perspective.Perspective import Perspective


class Start:
    def __init__(self, canvas_course_id, projects_groep_name, slb_groep_name,
                 start_date, end_date,
                 target_path, target_slb_path, attendance_report,
                 api_key, a_progress_levels, a_grade_levels):
        self.canvas_course_id = canvas_course_id
        self.api_key = api_key
        self.perspectives = {}
        self.roles = []
        self.progress_levels = a_progress_levels
        self.grade_levels = a_grade_levels
        self.projects_groep_name = projects_groep_name
        self.slb_groep_name = slb_groep_name
        self.start_date = start_date
        self.end_date = end_date
        self.target_path = target_path
        self.target_slb_path = target_slb_path
        self.attendance_report = attendance_report
        self.level_moments = None
        self.attendance = None

    def __str__(self):
        return f'Start({self.canvas_course_id}, {self.projects_groep_name}, {self.slb_groep_name}, {self.progress_levels}, {self.grade_levels}, {self.level_moments}, {self.attendance},  {self.start_date}, {self.end_date}, {self.progress_file_name}, {self.api_key})\n'

    def to_json(self, scope):
        dict_result = {
            'api_key': self.api_key,
            'canvas_course_id': self.canvas_course_id,
            'progress_levels': self.progress_levels,
            'grade_levels': self.grade_levels,
            'projects_groep_name': self.projects_groep_name,
            "slb_groep_name": self.slb_groep_name,
            'start_date': get_date_time_str(self.start_date),
            'end_date': get_date_time_str(self.end_date),
            'target_path': self.target_path,
            'target_slb_path': self.target_slb_path,
            'attendance_report': self.attendance_report,
            'perspectives': {},
            'roles': []
        }
        if self.attendance is not None:
            dict_result['attendance'] = self.attendance.to_json()
        else:
            dict_result['attendance'] = None
        if self.level_moments is not None:
            dict_result['level_moments'] = self.level_moments.to_json()
        else:
            dict_result['level_moments'] = None
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
                    get_date_time_obj(data_dict['start_date']),
                    get_date_time_obj(data_dict['end_date']),
                    data_dict['target_path'], data_dict['target_slb_path'],
                    data_dict['attendance_report'],
                    data_dict['api_key'],
                    data_dict['progress_levels'],
                    data_dict['grade_levels'])
        if 'level_moments' in data_dict.keys() and data_dict['level_moments'] is not None:
            new.level_moments = LevelMoments.from_dict(data_dict['level_moments'])
        if 'attendance' in data_dict.keys() and data_dict['attendance'] is not None:
            # print('Attendance', data_dict['attendance'])
            new.attendance = Attendance.from_dict(data_dict['attendance'])
        if data_dict['perspectives']:
            for key in data_dict['perspectives'].keys():
                new.perspectives[key] = Perspective.from_dict(data_dict['perspectives'][key])
        new.roles = list(map(lambda r: Role.from_dict(r), data_dict['roles']))
        return new

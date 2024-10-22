from lib.lib_date import get_date_time_obj, get_date_time_str

class Start:
    def __init__(self, canvas_course_id, projects_groep_name,
                 start_date, end_date, target_path, attendance_report, api_key):
        self.canvas_course_id = canvas_course_id
        self.api_key = api_key
        self.projects_groep_name = projects_groep_name
        self.start_date = start_date
        self.end_date = end_date
        self.target_path = target_path
        self.attendance_report = attendance_report

    def __str__(self):
        return f'Start({self.canvas_course_id}, {self.projects_groep_name},  {self.start_date}, {self.end_date}, {self.api_key})\n'

    def to_json(self, scope):
        dict_result = {
            'api_key': self.api_key,
            'canvas_course_id': self.canvas_course_id,
            'projects_groep_name': self.projects_groep_name,
            'start_date': get_date_time_str(self.start_date),
            'end_date': get_date_time_str(self.end_date),
            'target_path': self.target_path,
            'attendance_report': self.attendance_report,
        }
        return dict_result


    @staticmethod
    def from_dict(data_dict):
        new = Start(data_dict['canvas_course_id'],
                    data_dict['projects_groep_name'],
                    get_date_time_obj(data_dict['start_date']),
                    get_date_time_obj(data_dict['end_date']),
                    data_dict['target_path'],
                    data_dict['attendance_report'],
                    data_dict['api_key'])
        return new

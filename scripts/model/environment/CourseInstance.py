from scripts.lib.file_const import DIR_DIV

execution_source_path = "./courses/"

class CourseInstance:
    def __init__(self, name, course_code, canvas_course_id, target_path, period, stage):
        self.name = name
        self.course_code = course_code
        self.canvas_course_id = canvas_course_id
        self.target_path = target_path
        self.period = period
        self.stage = stage

    def to_json(self):
        dict_result = {
            'name': self.name,
            'course_code': self.course_code,
            'canvas_course_id': self.canvas_course_id,
            'target_path': self.target_path,
            'stage': self.stage,
            'period': self.period,
        }
        return dict_result

    def __str__(self):
        line = f' CourseInstance({self.course_code} {self.name} {self.canvas_course_id}, {self.stage})'
        return line

    def get_course_path(self):
        return execution_source_path + self.course_code + DIR_DIV

    def get_project_path(self):
        return execution_source_path + self.course_code + DIR_DIV + self.name + DIR_DIV

    def get_temp_path(self):
        return self.get_project_path() + "temp" + DIR_DIV

    def get_html_student_path(self):
        return self.get_project_path() + "dashboard" + DIR_DIV + self.name + DIR_DIV + "students" + DIR_DIV

    def get_link_student_path(self):
        return "." + DIR_DIV + self.name + DIR_DIV + "students" + DIR_DIV

    def get_html_general_path(self):
        return self.get_project_path() + "dashboard" + DIR_DIV + self.name + DIR_DIV + "general" + DIR_DIV

    def get_link_general_path(self):
        return "." + DIR_DIV + self.name + DIR_DIV + "general" + DIR_DIV

    def get_html_index_path(self):
        return self.get_project_path() + "dashboard" + DIR_DIV

    def get_config_file_name(self):
        return self.get_project_path() + "config_"+self.name +".json"

    def get_dashboard_file_name(self):
        return self.get_project_path() + "dashboard_"+self.name +".json"

    def get_course_file_name(self):
        return self.get_project_path() + "course_"+self.name +".json"

    def get_result_file_name(self):
        return self.get_project_path() + "result_"+self.name +".json"

    def get_progress_file_name(self):
        return self.get_project_path() + "progress_"+self.name +".json"

    def get_workload_file_name(self):
        return self.get_project_path() + "workload_"+self.name+".json"

    def get_trm_file_name(self):
        return self.get_project_path() + "trm_"+self.name+".xlsx"

    def get_user_data_file_name(self):
        return execution_source_path + "user_data.csv"

    def get_osiris_data_file_name(self):
        return self.get_project_path() + "osiris_data_"+self.name+".csv"

    def get_feedback_file_name(self, leaning_outcome):
        return self.get_project_path() + "feedback_"+self.name+"_"+leaning_outcome+".csv"

    def from_dict(data_dict):
        # print(data_dict)
        new = CourseInstance(data_dict["name"], data_dict["course_code"], data_dict["canvas_course_id"],
                             data_dict['target_path'], data_dict["period"], data_dict["stage"])
        return new

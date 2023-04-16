class CourseConfigStart:
    def __init__(self, course_id, config_file_name, api_key):
        self.course_id = course_id
        self.api_key = api_key
        self.config_file_name = config_file_name

    def __str__(self):
        return f'CourseConfigStart({self.course_id}, {self.config_file_name}, {self.api_key})'

    @staticmethod
    def from_dict(data_dict):
        return CourseConfigStart(data_dict['course_id'], data_dict['config_file_name'], data_dict['api_key'])


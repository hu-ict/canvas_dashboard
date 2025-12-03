from model.environment.CourseInstance import CourseInstance


class Course:
    def __init__(self, name):
        self.name = name
        self.course_instances = []

    def to_json(self):
        dict_result = {
            'name': self.name,
            'course_instances': list(map(lambda c: c.to_json(), self.course_instances))
        }
        return dict_result

    def __str__(self):
        return f' Course({self.name})'

    def get_course_instance_by_name(self, course_instance_name):
        for course_instance in self.course_instances:
            if course_instance.name == course_instance_name:
                return course_instance
        return None

    def get_path(self):
        return ".//courses//" + self.name + "//"

    @staticmethod
    def from_dict(data_dict):
        # print("CourseCategory", data_dict)
        new = Course(data_dict['name'])
        new.course_instances = list(map(lambda c: CourseInstance.from_dict(c), data_dict['course_instances']))
        return new

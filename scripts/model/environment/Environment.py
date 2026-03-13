from scripts.model.environment.Course import Course
from scripts.model.environment.Execution import Execution


class Environment:
    def __init__(self, name, current_instance_dict):
        self.current_instance = current_instance_dict
        self.name = name
        self.executions = []
        self.courses = []

    def to_json(self):
        return {'name': self.name, 'current_instance': self.current_instance,
                'executions': list(map(lambda e: e.to_json(), self.executions)),
                'courses': list(map(lambda c: c.to_json(), self.courses))}

    def __str__(self):
        return f'Environment({self.name})'

    def get_current_instance(self):
        for course in self.courses:
            for instance in course.course_instances:
                if instance.name == self.current_instance["course_instance_name"]:
                    return instance
        return None

    def get_course_names(self):
        names = []
        for course in self.courses:
            names.append(course.name)
        return names

    def get_course_by_name(self, course_name):
        for course in self.courses:
            if course.name == course_name:
                return course
        return None

    def get_execution_by_name(self, execution_name):
        for execution in self.executions:
            if execution.name == execution_name:
                return execution
        return None

    def is_instance_of_course(self, course_instance_name, course_name):
        for course in self.courses:
            if course.name == course_name:
                for course_instance in course.course_instances:
                    if course_instance.name == course_instance_name:
                        return True
        return False

    def get_instance_of_course(self, course_instance_dict):
        for course in self.courses:
            if course.name == course_instance_dict["course_name"]:
                for course_instance in course.course_instances:
                    if course_instance.name == course_instance_dict["course_instance_name"]:
                        return course_instance
        return None

    @staticmethod
    def from_dict(data_dict):
        # print("ENV02 -", data_dict)
        new = Environment(data_dict["name"], data_dict["current_instance"])
        if "executions" in data_dict:
            new.executions = list(map(lambda e: Execution.from_dict(e), data_dict['executions']))
        new.courses = list(map(lambda c: Course.from_dict(c), data_dict['courses']))
        return new

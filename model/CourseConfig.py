from model import Role
from model.AssignmentGroup import AssignmentGroup
from model.Section import Section
from model.StudentGroup import StudentGroup
from model.Teacher import Teacher


class CourseConfig:
    def __init__(self, course_id, name, api_key):
        self.name = name
        self.course_id = course_id
        self.api_key = api_key
        self.sections = []
        self.roles = []
        self.teachers = []
        self.assignmentGroups = []
        self.studentGroups = []

    def __str__(self):
        line = f'CourseConfig({self.course_id}, {self.name}, {self.api_key})\n'
        for section in self.sections:
            line += str(section)
        for teacher in self.teachers:
            line += str(teacher)
        for role in self.roles:
            line += str(role)
        for assignmentGroup in self.assignmentGroups:
            line += str(assignmentGroup)
        return line

    def to_json(self, scope):
        return {
            'course_id': self.course_id,
            'name': self.name,
            'api_key': self.api_key,
            'sections': list(map(lambda s: s.to_json(), self.sections)),
            'roles': list(map(lambda r: r.to_json([]), self.roles)),
            'teachers': list(map(lambda t: t.to_json(), self.teachers)),
            'assignment_groups': list(map(lambda a: a.to_json([]), self.assignmentGroups)),
            'student_groups': list(map(lambda g: g.to_json([]), self.studentGroups)),
        }

    def find_assignment_group(self, group_id):
        for group in self.assignmentGroups:
            if group.id == group_id:
                return group

    def find_assignment_group_by_name(self, group_name):
        for group in self.assignmentGroups:
            if group.name == group_name:
                return group

    def find_assignment_group_by_role(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return self.find_assignment_group(role.assignment_group_id)

    def find_role(self, role_names):
        for role_name in role_names:
            if role_name != "INNO":
                for role in self.roles:
                    if role.name == role_name:
                        return role

    def find_student_group(self, group_id):
        for group in self.studentGroups:
            if group.id == group_id:
                return group
        return "Geen"

    def find_teacher_by_group(self, group_id):
        for teacher in self.teachers:
            if group_id in teacher.projects:
                return teacher

    @staticmethod
    def from_dict(data_dict):
        new_course_config = CourseConfig(data_dict['course_id'], data_dict['name'], data_dict['api_key'])
        new_course_config.sections = list(map(lambda s: Section.from_dict(s), data_dict['sections']))
        new_course_config.teachers = list(map(lambda t: Teacher.from_dict(t), data_dict['teachers']))
        new_course_config.roles = list(map(lambda r: Role.from_dict(r), data_dict['roles']))
        new_course_config.assignmentGroups = list(map(lambda g: AssignmentGroup.from_dict(g), data_dict['assignment_groups']))
        new_course_config.studentGroups = list(map(lambda s: StudentGroup.from_dict(s), data_dict['student_groups']))
        return new_course_config

from lib.lib_date import get_date_time_obj, get_date_time_str
from model.AssignmentGroup import AssignmentGroup
from model.Role import Role
from model.Section import Section
from model.Student import Student
from model.StudentGroup import StudentGroup
from model.StudentLink import StudentLink
from model.Teacher import Teacher
from model.perspective.Attendance import Attendance
from model.perspective.Level import Level
from model.perspective.LevelMoments import LevelMoments
from model.perspective.Perspective import Perspective
from model.perspective.Perspectives import Perspectives


class CourseConfig:
    def __init__(self, name, days_in_semester, student_count):
        self.name = name
        self.student_count = student_count
        self.days_in_semester = days_in_semester
        self.sections = []
        self.level_moments = None
        self.attendance = None
        self.perspectives = {}
        self.roles = []
        self.teachers = []
        self.assignment_groups = []
        self.student_groups = []
        self.role_groups = []
        self.slb_groups = []
        self.students = []

    def __str__(self):
        line = f'CourseConfig({self.name})\n'
        for section in self.sections:
            line += str(section)
        for teacher in self.teachers:
            line += str(teacher)
        for role in self.roles:
            line += str(role)
        line += str(self.perspectives)
        for assignment_group in self.assignment_groups:
            line += str(assignment_group)
        for student_group in self.student_groups:
            line += str(student_group)
        for slb_group in self.slb_groups:
            line += str(slb_group)
        for student in self.students:
            line += str(student)
        return line

    def to_json(self, scope):
        dict_result = {
            'name': self.name,
            'student_count': self.student_count,
            'days_in_semester': self.days_in_semester,
            'sections': list(map(lambda s: s.to_json(), self.sections))
        }
        if self.attendance is not None:
            dict_result['attendance'] = self.attendance.to_json()
        else:
            dict_result['attendance'] = None
        if self.level_moments is not None:
            dict_result['level_moments'] = self.level_moments.to_json()
        else:
            dict_result['level_moments'] = None
        dict_result['perspectives'] = {}
        for key in self.perspectives:
            dict_result['perspectives'][key] = self.perspectives[key].to_json()
        dict_result['roles'] = list(map(lambda r: r.to_json([]), self.roles))
        dict_result['teachers'] = list(map(lambda t: t.to_json(), self.teachers))
        dict_result['assignment_groups'] = list(map(lambda ag: ag.to_json(scope), self.assignment_groups))
        dict_result['student_groups'] = list(map(lambda sg: sg.to_json([]), self.student_groups))
        dict_result['slb_groups'] = list(map(lambda sg: sg.to_json([]), self.slb_groups))
        dict_result['students'] = list(map(lambda s: s.to_json(['perspectives']), self.students))

        return dict_result

    def find_student_group(self, group_id):
        for group in self.student_groups:
            if group.id == group_id:
                return group
        return None

    def find_student_group_by_name(self, group_name):
        for group in self.student_groups:
            if group.name == group_name:
                return group
        return None

    def find_students_by_role(self, role_short):
        students = []
        for student in self.students:
            if student.role == role_short:
                students.append(student)
        return students

    def find_slb_group(self, slb_group_id):
        for group in self.slb_groups:
            if group.id == slb_group_id:
                return group
        return None

    def find_assignment_group(self, group_id):
        for group in self.assignment_groups:
            if group.id == group_id:
                return group
        return None

    def find_assignment(self, assignment_id):
        for assignment_group in self.assignment_groups:
            for assignment_sequence in assignment_group.assignment_sequences:
                for assignment in assignment_sequence.assignments:
                    if assignment.id == assignment_id:
                        return assignment
        return None

    def find_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def find_student_by_name(self, student_name):
        for student in self.students:
            if student.name == student_name:
                return student
        return None

    def remove_student_by_name(self, student_name):
        for student in self.students:
            if student.name == student_name:
                self.students.remove(student)
                return student.name
        return None

    def find_teacher(self, teacher_id):
        for teacher in self.teachers:
            if teacher_id == teacher.id:
                return teacher
        return None

    def find_section(self, section_id):
        for section in self.sections:
            if section_id == section.id:
                return section
        return None

    def get_submission_perspectives(self):
        return None

    def find_perspective_by_name(self, name):
        for perspective in self.perspectives.values():
            if name == perspective.name:
                return perspective
        return None

    def find_perspective_by_assignment_group(self, assignment_group_id):
        for perspective in self.perspectives.values():
            if assignment_group_id in perspective.assignment_groups:
                return perspective
        if self.level_moments is not None and assignment_group_id in self.level_moments.assignment_groups:
            return self.level_moments
        if self.attendance is not None and assignment_group_id in self.attendance.assignment_groups:
            return self.attendance
        return None

    def find_assignment_group_by_name(self, group_name):
        print(group_name)
        for group in self.assignment_groups:
            print("find_assignment_group_by_name", group_name, group)
            if group.name == group_name:
                return group
        return None

    def find_assignment_group_by_role(self, a_role):
        # print("find_assignment_group_by_role", a_role)
        for role in self.roles:
            if role.short == a_role:
                return role.assignment_groups[0]
        return None

    def find_assignment_by_group(self, assigment_group_id, assignment_id):
        assignment_group = self.find_assignment_group(assigment_group_id)
        if not assignment_group:
            return None
        for assigment in assignment_group.assignments:
            if assigment.id == assignment_id:
                return assigment
        return None

    def find_assignment_group_by_role_name(self, role_name):
        for role in self.roles:
            if role.name == role_name:
                return self.find_assignment_group(role.assignment_group_id)
        return None

    def get_level_moments_by_query(self, a_query):
        for assignment_group_id in self.level_moments.assignment_groups:
            assignment_group = self.find_assignment_group(assignment_group_id)
            for assignment in assignment_group.assignment_sequences:
                condition = 0
                for selector in a_query:
                    if selector.lower() in assignment.name.lower():
                        condition += 1
                if condition == len(a_query):
                    return assignment
        return None

    def get_role(self, role_short):
        for role in self.roles:
            if role.short == role_short:
                return role
        return None

    def find_role_by_section(self, section_id):
        for section in self.sections:
            if section.id == section_id:
                return section.role
        return None

    def find_teacher_by_group(self, group_id):
        for teacher in self.teachers:
            if group_id in teacher.projects:
                return teacher
        return None

    @staticmethod
    def from_dict(data_dict):
        new = CourseConfig(
            data_dict['name'],
            data_dict['days_in_semester'],
            data_dict['student_count'])
        new.perspectives = {}
        if 'level_moments' in data_dict.keys() and data_dict['level_moments'] is not None:
            new.level_moments = LevelMoments.from_dict(data_dict['level_moments'])
        if 'attendance' in data_dict.keys() and data_dict['attendance'] is not None:
            new.attendance = Attendance.from_dict(data_dict['attendance'])
        if 'perspectives' in data_dict.keys():
            for key in data_dict['perspectives'].keys():
                new.perspectives[key] = Perspective.from_dict(data_dict['perspectives'][key])
        new.sections = list(map(lambda s: Section.from_dict(s), data_dict['sections']))
        new.teachers = list(map(lambda t: Teacher.from_dict(t), data_dict['teachers']))

        new.judgement = {}
        new.roles = list(map(lambda r: Role.from_dict(r), data_dict['roles']))
        new.assignment_groups = list(
            map(lambda g: AssignmentGroup.from_dict(g), data_dict['assignment_groups']))
        new.student_groups = list(map(lambda s: StudentGroup.from_dict(s), data_dict['student_groups']))
        new.slb_groups = list(map(lambda s: StudentGroup.from_dict(s), data_dict['slb_groups']))
        new.students = list(map(lambda s: Student.from_dict(s), data_dict['students']))
        return new

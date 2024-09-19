from model.perspective.AttendancePerspective import AttendancePerspective
from model.perspective.StudentLevelMoments import StudentLevelMoments
from model.perspective.StudentPerspective import StudentPerspective


class Student:
    def __init__(self, a_student_id, a_group_id, a_name, a_number, a_sortable_name, a_coach, a_role, a_email, a_site, a_progress):
        self.id = a_student_id
        self.group_id = a_group_id
        self.name = a_name
        self.number = a_number
        self.sortable_name = a_sortable_name
        self.coach = a_coach
        self.email = a_email
        self.site = a_site
        self.progress = a_progress
        self.role = a_role
        self.student_level_moments = None
        self.attendance_perspective = None
        self.perspectives = None

    def __str__(self):
        line = f'Student({self.id}, {self.group_id}, {self.name}, {self.number}, {self.coach}, {self.role}, {self.email}, {self.progress})\n'
        if self.perspectives is not None:
            for perspective in self.perspectives:
                line += " p "+str(self.perspectives[perspective])
        line += " a "+str(self.attendance_perspective)
        return line

    def get_perspective(self, name):
        for perspective in self.perspectives:
            if perspective.name == name:
                return perspective
        return None

    def get_peilmoment(self, assigment_id):
        for peilmoment in self.student_level_moments.submissions:
            if peilmoment.assignment_id == assigment_id:
                return peilmoment
        return None

    def get_peilmoment_submission_by_query(self, a_query):
        for submission in self.student_level_moments.submissions:
            condition = 0
            for selector in a_query:
                if selector.lower() in submission.assignment_name.lower():
                    condition += 1
            if condition == len(a_query):
                return submission
        return None

    def get_judgement(self, perspective_name):
        for level_moment in self.student_level_moments.submissions:
            if perspective_name in level_moment.assignment_name.lower() and "beoordeling" in level_moment.assignment_name.lower():
                return int(level_moment.score)
        return None


    def to_json(self, scope):
        dict_result = {
            'name': self.name,
            'id': self.id,
            'number': self.number,
            'sortable_name': self.sortable_name,
            'group_id': self.group_id,
            'coach': self.coach,
            'email': self.email,
            'site': self.site,
            'role': self.role,
            'progress': self.progress,
            'perspectives': {}
        }
        if self.student_level_moments is not None:
            dict_result['student_level_moments'] = self.student_level_moments.to_json()
        if self.attendance_perspective is not None:
            dict_result['attendance_perspective'] = self.attendance_perspective.to_json()
        if "perspectives" in scope:
            for key in self.perspectives:
                dict_result['perspectives'][key] = self.perspectives[key].to_json()
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        # print("Student.from_dict", data_dict)
        if 'number' in data_dict.keys():
            new = Student(data_dict['id'], data_dict['group_id'], data_dict['name'], data_dict['number'], data_dict['sortable_name'], data_dict['coach'],
            data_dict['role'], data_dict['email'], data_dict[ 'site'], data_dict['progress'])
        else:
            new = Student(data_dict['id'], data_dict['group_id'], data_dict['name'], "x", data_dict['sortable_name'], data_dict['coach'],
            data_dict['role'], data_dict['email'], data_dict[ 'site'], data_dict['progress'])

        if 'student_level_moments' in data_dict.keys() and data_dict['student_level_moments'] is not None:
            new.student_level_moments = StudentLevelMoments.from_dict(data_dict['student_level_moments'])
        if 'attendance_perspective' in data_dict.keys() and data_dict['attendance_perspective'] is not None:
            new.attendance_perspective = AttendancePerspective.from_dict(data_dict['attendance_perspective'])
        new.perspectives = {}
        if 'perspectives' in data_dict.keys():
            for key in data_dict['perspectives'].keys():
                new.perspectives[key] = StudentPerspective.from_dict(data_dict['perspectives'][key])
        return new

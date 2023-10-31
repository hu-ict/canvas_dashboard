from model.perspective.StudentPerspective import StudentPerspective
from model.perspective.StudentPerspectives import StudentPerspectives


class Student:
    def __init__(self, a_student_id, a_group_id, a_name, a_coach_initials, a_role, a_email, a_site, a_progress):
        self.id = a_student_id
        self.group_id = a_group_id
        self.name = a_name
        self.coach_initials = a_coach_initials
        self.email = a_email
        self.site = a_site
        self.progress = a_progress
        self.role = a_role
        self.perspectives = {}

    # def get_perspective(self, name):
    #     for perspective in self.perspectives:
    #         if perspective.name == name:
    #             return perspective
    #     return None

    def get_peilmoment(self, assigment_id):
        for peilmoment in self.perspectives.perspectives["peil"].submissions:
            if peilmoment.assignment_id == assigment_id:
                return peilmoment
        return None

    def to_json(self, scope):
        if "submissions" in scope:
            return {
                'name': self.name,
                'id': self.id,
                'group_id': self.group_id,
                'coach_initials': self.coach_initials,
                'email': self.email,
                'site': self.site,
                'progress': self.progress,
                'role': self.role,
                'perspectives': self.perspectives.to_json()
            }
        else:
            return {
                'name': self.name,
                'id': self.id,
                'group_id': self.group_id,
                'coach_initials': self.coach_initials,
                'email': self.email,
                'site': self.site,
                'progress': self.progress,
                'role': self.role,
                'perspectives': self.perspectives.to_json()
            }

    def __str__(self):
        line = f'Student({self.id}, {self.group_id}, {self.name}, {self.coach_initials}, {self.role}, {self.email}, {self.progress})\n'
        for perspective in self.perspectives.perspectives:
            line += " p "+str(self.perspectives.perspectives[perspective])
        return line

    @staticmethod
    def from_dict(data_dict):
        # print("Student.from_dict", data_dict)
        new_student = Student(data_dict['id'], data_dict['group_id'], data_dict['name'], data_dict['coach_initials'],
                              data_dict['role'], data_dict['email'], data_dict[ 'site'], data_dict[ 'progress'])
        if data_dict['perspectives']:
            new_student.perspectives = StudentPerspectives.from_dict(data_dict['perspectives'])
        else:
            new_student.perspectives = {}
        return new_student

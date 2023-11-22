from model.perspective.StudentPerspective import StudentPerspective


class Student:
    def __init__(self, a_student_id, a_group_id, a_name, a_sortable_name, a_coach, a_role, a_email, a_site, a_progress):
        self.id = a_student_id
        self.group_id = a_group_id
        self.name = a_name
        self.sortable_name = a_sortable_name
        self.coach = a_coach
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
        for peilmoment in self.perspectives["peil"].submissions:
            if peilmoment.assignment_id == assigment_id:
                return peilmoment
        return None

    def to_json(self, scope):
        dict_result = {
            'name': self.name,
            'id': self.id,
            'sortable_name': self.sortable_name,
            'group_id': self.group_id,
            'coach': self.coach,
            'email': self.email,
            'site': self.site,
            'role': self.role,
            'progress': self.progress,
            'perspectives': {}
        }
        if "submissions" in scope:
            for key in self.perspectives:
                dict_result['perspectives'][key] = self.perspectives[key].to_json()
        return dict_result

    def __str__(self):
        line = f'Student({self.id}, {self.group_id}, {self.name}, {self.coach}, {self.role}, {self.email}, {self.progress})\n'
        for perspective in self.perspectives:
            line += " p "+str(self.perspectives[perspective])
        return line

    @staticmethod
    def from_dict(data_dict):
        # print("Student.from_dict", data_dict)
        new = Student(data_dict['id'], data_dict['group_id'], data_dict['name'], data_dict['sortable_name'], data_dict['coach'],
            data_dict['role'], data_dict['email'], data_dict[ 'site'], data_dict['progress'])
        if data_dict['perspectives']:
            for key in data_dict['perspectives'].keys():
                new.perspectives[key] = StudentPerspective.from_dict(data_dict['perspectives'][key])
        else:
            new.perspectives = {}
        return new

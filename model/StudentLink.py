from model.perspective.StudentProgress import StudentProgress
from model.perspective.StudentPerspective import StudentPerspective


class StudentLink:
    def __init__(self, a_student_id, a_name, a_sortable_name):
        self.id = a_student_id
        self.name = a_name
        self.sortable_name = a_sortable_name


    def to_json(self, scope):
        return {
            'name': self.name,
            'id': self.id,
            'sortable_name': self.sortable_name
        }

    def __str__(self):
        return f'StudentLink({self.id}, {self.name})'

    @staticmethod
    def from_student(student):
        return StudentLink(student.id, student.name, student.sortable_name)

    @staticmethod
    def from_dict(data_dict):
        # print("Student.from_dict", data_dict)
        return StudentLink(data_dict['id'], data_dict['name'], data_dict['sortable_name'])


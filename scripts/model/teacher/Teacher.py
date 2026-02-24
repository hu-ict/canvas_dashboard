from scripts.model.teacher.Responsibility import Responsibility


class Teacher:
    def __init__(self, teacher_id, name, email):
        self.id = teacher_id
        self.name = name
        self.initials = ''.join([x[0].upper() for x in name.split(' ')])
        self.email = email
        self.responsibilities = []

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'responsibilities': list(map(lambda r: r.to_json(), self.responsibilities))
        }

    def __str__(self):
        return f'Teacher({self.id}, {self.name}, {self.initials}, {self.email})'

    def find_responsibility_by_assignment_group_id(self, assignment_group_id):
        for responsibility in self.responsibilities:
            if responsibility.assignment_group_id == assignment_group_id:
                return responsibility
        return None

    def put_responsibility(self, canvas_group, group_name, assignment_group_id):
        l_responsibility = self.find_responsibility_by_assignment_group_id(assignment_group_id)
        if l_responsibility:
            l_responsibility.student_groups.append(group_name)
        else:
            self.responsibilities.append(Responsibility(canvas_group, [group_name], assignment_group_id))

    @staticmethod
    def from_dict(data_dict):
        if 'email' in data_dict:
            new_teacher = Teacher(data_dict['id'], data_dict['name'], data_dict["email"])
        else:
            new_teacher = Teacher(data_dict['id'], data_dict['name'], "")
        if 'responsibilities' in data_dict:
            # print("TE41 - read responsibilities", new_teacher.name, data_dict['responsibilities'])
            new_teacher.responsibilities = list(map(lambda r: Responsibility.from_dict(r), data_dict['responsibilities']))
        return new_teacher

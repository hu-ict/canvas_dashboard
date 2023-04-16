class Role:
    def __init__(self, name, description, assignment_group_id, btn_color):
        self.name = name
        self.description = description
        self.assignment_group_id = assignment_group_id
        self.btn_color = btn_color
        self.sections = []

    def to_json(self, scope):
        return {
            'description': self.description,
            'name': self.name,
            'assignment_group_id': self.assignment_group_id,
            'btn_color': self.btn_color,
            'sections': list(map(lambda s: s.to_json(), self.sections)),
        }

    def __str__(self):
        line = f'  Role({self.name}, {self.description}, {self.assignment_group_id}, {self.btn_color}, {self.sections})\n'
        return line

def from_dict(data_dict):
    new_role = Role(data_dict['name'], data_dict['description'], data_dict['assignment_group_id'], data_dict['btn_color'])
    new_role.sections = list(map(lambda s: s, data_dict['sections']))
    return new_role

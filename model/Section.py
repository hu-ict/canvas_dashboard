class Section:
    def __init__(self, section_id, name, role):
        self.id = section_id
        self.name = name
        self.role = role

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role
        }

    def __str__(self):
        line = f' Section({self.id}, {self.name}, {self.role})'
        return line

    @staticmethod
    def from_dict(data_dict):
        return Section(data_dict['id'], data_dict['name'], data_dict['role'])

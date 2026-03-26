class Groups:
    def __init__(self, title, name, principal_assignment_group):
        self.title = title
        self.name = name
        self.principal_assignment_group = principal_assignment_group

    def to_json(self):
        return {
            'title': self.title,
            'name': self.name,
            'principal_assignment_group': self.principal_assignment_group
        }

    def __str__(self):
        return f'Groups({self.title}, {self.name}, {self.principal_assignment_group})'

    @staticmethod
    def from_dict(data_dict):
        # print("GR01 -", data_dict)
        new = Groups(data_dict['title'], data_dict['name'], data_dict['principal_assignment_group'])
        return new


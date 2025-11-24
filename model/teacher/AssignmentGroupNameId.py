class AssignmentGroupNameId:
    def __init__(self, assignment_group_id, name, groups):
        self.id = assignment_group_id
        self.name = name
        self.groups = groups

    def to_json(self):
        json_string = {
            'name': self.name,
            'id': self.id,
            'groups': self.groups
        }
        return json_string

    def __str__(self):
        line = f'AssigmentGroupNameId({self.id}, {self.name}, {self.groups})'
        return line

    @staticmethod
    def from_dict(data_dict):
        new = AssignmentGroupNameId(data_dict['id'], data_dict['name'], data_dict['groups'])
        return new

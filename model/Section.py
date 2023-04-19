class Section:
    def __init__(self, section_id, name):
        self.name = name
        self.id = section_id

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __str__(self):
        line = f' Section({self.id}, {self.name})\n'
        return line


    @staticmethod
    def from_dict(data_dict):
        return Section(data_dict['id'], data_dict['name'])

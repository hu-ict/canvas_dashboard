class MetaLevelMoments:
    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.levels = "progress"
        self.assignment_group_names = []

    def to_json(self):
        dict_result = {
            'name': self.name,
            'title': self.title,
            'assignment_group_names': self.assignment_group_names
        }
        return dict_result

    def __str__(self):
        return f'LevelMoments({self.name}, {self.title}, {self.assignment_group_names})'

    @staticmethod
    def from_dict(data_dict):
        print("Perspective.from_dict", data_dict)
        new = MetaLevelMoments(data_dict['name'], data_dict['title'])
        if 'assignment_group_names' in data_dict.keys():
            new.assignment_group_names = data_dict['assignment_group_names']
        return new

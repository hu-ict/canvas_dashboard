class LevelMoments:
    def __init__(self, name, title):
        self.name = name
        self.title = title
        self.levels = "progress"
        self.assignment_group_ids = []

    def to_json(self):
        dict_result = {
            'name': self.name,
            'title': self.title,
            'assignment_group_ids': self.assignment_group_ids
        }
        return dict_result

    def __str__(self):
        return f'LevelMoments({self.name}, {self.title}, {self.assignment_group_ids})'

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        new = LevelMoments(data_dict['name'], data_dict['title'])
        if 'assignment_group_ids' in data_dict.keys():
            new.assignment_group_ids = data_dict['assignment_group_ids']
        return new

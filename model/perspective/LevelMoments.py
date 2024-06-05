class LevelMoments:
    def __init__(self, name, title, levels, moments):
        self.name = name
        self.title = title
        self.levels = levels
        self.moments = moments
        self.assignment_groups = []

    def to_json(self):
        dict_result = {
            'name': self.name,
            'title': self.title,
            'levels': self.levels,
            'moments': self.moments,
            'assignment_groups': self.assignment_groups
        }
        return dict_result

    def __str__(self):
        return f'LevelMoments({self.name}, {self.title}, {self.levels}, {self.moments}, {self.assignment_groups})'

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        new = LevelMoments(data_dict['name'], data_dict['title'], data_dict['levels'], data_dict['moments'])
        if 'assignment_groups' in data_dict.keys():
            new.assignment_groups = data_dict['assignment_groups']
        return new

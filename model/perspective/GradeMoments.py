class GradeMoments:
    def __init__(self, name, title, levels, moments):
        self.name = name
        self.title = title
        self.levels = levels
        self.moments = moments
        self.assignment_group_ids = []

    def to_json(self):
        dict_result = {
            'name': self.name,
            'title': self.title,
            'levels': self.levels,
            'moments': self.moments,
            'assignment_groups': self.assignment_group_ids
        }
        return dict_result

    def __str__(self):
        return f'GradeMoments({self.name}, {self.title}, {self.levels}, {self.moments}, {self.assignment_group_ids})'

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        new = GradeMoments(data_dict['name'], data_dict['title'], data_dict['levels'], data_dict['moments'])
        if 'assignment_groups' in data_dict.keys():
            new.assignment_group_ids = data_dict['assignment_groups']
        return new

class MetaPerspective:
    def __init__(self, name, title, show_flow, show_points, assignment_group_names):
        self.name = name
        self.title = title
        self.show_points = show_points
        self.show_flow = show_flow
        self.assignment_group_names = assignment_group_names

    def to_json(self):
        dict_result = {
            'name': self.name,
            'title': self.title,
            'show_flow': self.show_flow,
            'show_points': self.show_points,
            'assignment_group_names': self.assignment_group_names

        }
        return dict_result

    def __str__(self):
        return f'MetaPerspective({self.name}, {self.title}, {self.assignment_group_names})'

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        new = MetaPerspective(data_dict['name'], data_dict['title'], data_dict['show_flow'], data_dict['show_points'],
                          data_dict['assignment_group_names'])
        return new

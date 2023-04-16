class Assignment:
    def __init__(self, id, name, group_id, points, date_at, score):
        self.id = id
        self.name = name
        self.group_id = group_id
        self.points = points
        self.date_at = date_at
        self.score = score


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'group_id': self.group_id,
            'points': self.points,
            'date_at': self.date_at,
            'score': self.score
        }

    def __str__(self):
        return f'Assigment({self.id}, {self.name}, {self.points}, {self.date_at}, {self.score})'

    @staticmethod
    def from_dict(data_dict):
        return Assignment(data_dict['id'], data_dict['name'], data_dict['group_id'], data_dict['points'], data_dict['date_at'], data_dict['score'])

class Rating:
    def __init__(self, id, points, description):
        self.id = id
        self.points = points
        self.description = description

    def to_json(self):
        return {
            'id': self.id,
            'points': self.points,
            'description': self.description,
        }

    def __str__(self):
        return f'Rating({self.id}, {self.points}, {self.description}'

    @staticmethod
    def from_dict(data_dict):
        return Rating(data_dict['id'], data_dict['points'], data_dict['description'])

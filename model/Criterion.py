from model.Rating import Rating


class Criterion:
    def __init__(self, criterion_id, points, description):
        self.id = criterion_id
        self.points = points
        self.description = description
        self.ratings = []

    def get_rating(self, rating_id):
        for rating in self.ratings:
            if rating.id == rating_id:
                return rating
        print("CR01", rating_id)
        return None

    def to_json(self):
        return {
            'id': self.id,
            'points': self.points,
            'description': self.description,
            'ratings': list(map(lambda r: r.to_json(), self.ratings)),
        }

    def __str__(self):
        str_ratings = ""
        for rating in self.ratings:
            str_ratings += "\n"+str(rating)
        return f'Criterion(Id: {self.id}, {self.points}, {self.description})'+str_ratings

    @staticmethod
    def from_dict(data_dict):
        new = Criterion(data_dict['id'], data_dict['points'], data_dict['description'])
        new.ratings = list(map(lambda c: Rating.from_dict(c), data_dict['ratings']))
        return new

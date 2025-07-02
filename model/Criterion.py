from model.Rating import Rating


class Criterion:
    def __init__(self, criterion_id, points, description):
        self.id = criterion_id
        self.points = points
        self.description = description
        self.ratings = []
        self.learning_outcomes = []

    def get_rating(self, rating_id):
        for rating in self.ratings:
            if rating.id == rating_id:
                return rating
        print("CR01", rating_id)
        return None

    def add_learning_outcome(self, learning_outcome_id):
        if learning_outcome_id not in self.learning_outcomes:
            self.learning_outcomes.append(learning_outcome_id)

    def to_json(self):
        return {
            'id': self.id,
            'points': self.points,
            'description': self.description,
            'ratings': list(map(lambda r: r.to_json(), self.ratings)),
            'learning_outcomes': self.learning_outcomes
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
        if 'learning_outcomes' in data_dict:
            new.learning_outcomes = data_dict['learning_outcomes']
        return new

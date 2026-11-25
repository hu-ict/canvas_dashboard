class SaturationPortfolioItemLearningOutcome:
    def __init__(self, learning_outcome_id):
        self.id = learning_outcome_id
        self.collection = []

    def to_json(self):
        return {
            'id': self.id,
            'collection': list(map(lambda lu: lu.to_json(), self.collection))
        }

    def __str__(self):
        return f'SaturationPortfolioItemLearningOutcome(Id: {self.id}, {len(self.collection)})'

    @staticmethod
    def from_dict(data_dict):
        new = SaturationPortfolioItemLearningOutcome(data_dict['id'])
        new.last_day_collection = data_dict['last_day_collection']
        for item in data_dict['collection']:
            new.collection.append(SaturationPortfolioItemLearningOutcome.from_dict(item))
        return new

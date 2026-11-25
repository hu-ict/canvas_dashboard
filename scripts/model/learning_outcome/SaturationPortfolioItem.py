import statistics

from scripts.model.learning_outcome.SaturationPortfolioItemLearningOutcome import SaturationPortfolioItemLearningOutcome

class SaturationPortfolioItem:
    def __init__(self, assignment_id, name, day):
        self.id = assignment_id
        self.name = name
        self.day = day
        self.collection = []
        self.learning_outcomes = []

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'day': self.day,
            'collection': self.collection,
            'learning_outcomes': list(map(lambda lu: lu.to_json(), self.learning_outcomes))
        }

    def __str__(self):
        return f'SaturationPortfolioItem(Id: {self.id}, {self.name}, {self.day}, {len(self.collection)}, min: {round(self.get_min_stdv(), 2)}, average: {round(self.get_average_lu(), 2)}, plus: {round(self.get_plus_stdv(), 2)})'

    def get_average_lu(self):
        length = len(self.collection)
        if length > 0:
            return sum(self.collection)/length
        else:
            return 0

    def get_min_stdv(self):
        if len(self.collection) > 2:
            stdv = statistics.stdev(self.collection)
            min_stdv = self.get_average_lu() - stdv
            if min_stdv < 0:
                min_stdv = 0
            return round(min_stdv, 2)
        else:
            return 0

    def get_plus_stdv(self):
        if len(self.collection) > 2:
            stdv = statistics.stdev(self.collection)
            plus_stdv = self.get_average_lu() + stdv
            if plus_stdv < 0:
                plus_stdv = 0
            return round(plus_stdv, 2)
        else:
            return 0

    def get_diff(self, comparable):
        if comparable > 0:
            result =  self.get_average_lu() / comparable
            if result < 1:
                result = -1 + result
            else:
                result = 1 - (comparable / self.get_average_lu())
            return round(result, 2)
        else:
            return round(0, 2)

    @staticmethod
    def from_dict(data_dict):
        new = SaturationPortfolioItem(data_dict['id'], data_dict['name'], data_dict['day'])
        new.collection = data_dict['collection']
        for learning_outcome in data_dict['learning_outcomes']:
            new.learning_outcomes.append(SaturationPortfolioItemLearningOutcome.from_dict(learning_outcome))
        return new

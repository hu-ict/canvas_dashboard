class CriteriumScore:
    def __init__(self, criterion_score_id, rating_id, score, comment):
        self.id = criterion_score_id
        self.rating_id = rating_id
        self.score = score
        self.comment = comment

    def to_json(self):
        return {
            'id': self.id,
            'rating_id': self.rating_id,
            'score': self.score,
            'comment': self.comment,
        }

    def __str__(self):
        return f'CriteriumScore({self.id}, Rating: {self.rating_id}, Score: {self.score}, Comment: {self.comment})'

    @staticmethod
    def from_dict(data_dict):
        return CriteriumScore(data_dict['id'], data_dict['rating_id'], data_dict['score'], data_dict['comment'])

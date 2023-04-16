class Statistics:
    def __init__(self, submission_count, not_graded_count):
        self.submission_count = submission_count
        self.not_graded_count = not_graded_count

    def to_json(self):
        return {
            'submission_count': self.submission_count,
            'not_graded_count': self.not_graded_count
        }

    def __str__(self):
        return f'Comment({self.submission_count}, {self.not_graded_count}'

    @staticmethod
    def from_dict(data_dict):
        return Statistics(data_dict['submission_count'], data_dict['not_graded_count'])

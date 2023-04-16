class Comment:
    def __init__(self, author_id, author_name, comment):
        self.author_id = author_id
        self.author_name = author_name
        self.comment = comment

    def to_json(self):
        return {
            'author_id': self.author_id,
            'author_name': self.author_name,
            'comment': self.comment,
        }

    def __str__(self):
        return f'Comment({self.author_id}, {self.author_name}, {self.comment}'

    @staticmethod
    def from_dict(data_dict):
        return Comment(data_dict['author_id'], data_dict['author_name'], data_dict['comment'])

from lib.config import get_date_time_obj, get_date_time_str


class Comment:
    def __init__(self, author_id, author_name, date, comment):
        self.author_id = author_id
        self.author_name = author_name
        self.date = date
        self.comment = comment

    def to_json(self):
        return {
            'author_id': self.author_id,
            'author_name': self.author_name,
            'date': get_date_time_str(self.date),
            'comment': self.comment,
        }

    def __str__(self):
        return f'Comment({self.author_id}, {self.author_name}, {self.date}, {self.comment}'

    @staticmethod
    def from_dict(data_dict):
        return Comment(data_dict['author_id'], data_dict['author_name'], get_date_time_obj(data_dict['date']), data_dict['comment'])

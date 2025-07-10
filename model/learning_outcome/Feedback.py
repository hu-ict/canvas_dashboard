from lib.lib_date import get_date_time_obj, get_date_time_str


class Feedback:
    def __init__(self, author_id, author_name, date, day, comment, assignment_name, submission_id, grade):
        self.author_id = author_id
        self.author_name = author_name
        self.date = date
        self.day = day
        self.comment = comment
        self.assignment_name = assignment_name
        self.submission_id = submission_id
        self.grade = grade

    def to_json(self):
        return {
            'author_id': self.author_id,
            'author_name': self.author_name,
            'date': get_date_time_str(self.date),
            'day': self.day,
            'comment': self.comment,
            'assignment_name': self.assignment_name,
            'submission_id': self.submission_id,
            'grade': self.grade
        }

    def __str__(self):
        return f'Feedback({self.author_id}, {self.author_name}, {self.date}, {self.comment}, {self.assignment_name}, {self.submission_id}, {self.grade}'

    @staticmethod
    def from_dict(data_dict):
        return Feedback(data_dict['author_id'], data_dict['author_name'], get_date_time_obj(data_dict['date']), data_dict['day'], data_dict['comment'], data_dict['assignment_name'], data_dict['submission_id'], data_dict['grade'])

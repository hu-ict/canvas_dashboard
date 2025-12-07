from scripts.lib.lib_date import get_date_time_obj, get_date_time_str


class SubmissionAssignment:
    def __init__(self, assignment_id, name, group_id, points, date, day):
        self.id = assignment_id
        self.name = name
        self.group_id = group_id
        self.points = points
        self.date = date
        self.day = day

    def __str__(self):
        return f'SubmissionAssignment({self.id}, {self.name}, {self.group_id}, {self.points}, ' \
               f'{get_date_time_str(self.date)}, {self.day})'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'group_id': self.group_id,
            'points': int(self.points),
            'date': get_date_time_str(self.date),
            'day': self.day
        }

    @staticmethod
    def from_dict(data_dict):
        new = SubmissionAssignment(data_dict['id'], data_dict['name'], data_dict['group_id'], data_dict['points'],
                                   get_date_time_obj(data_dict['date']), data_dict['day'])
        return new

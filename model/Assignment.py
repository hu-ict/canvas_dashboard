from lib.config import get_date_time_obj, get_date_time_str


class Assignment:
    def __init__(self, id, name, group_id, course_section_id, points, assignment_date, unlock_date):
        self.id = id
        self.name = name
        self.group_id = group_id
        self.course_section_id = course_section_id
        self.points = points
        self.assignment_date = assignment_date
        self.unlock_date = unlock_date


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'group_id': self.group_id,
            'points': self.points,
            'course_section_id': self.course_section_id,
            'assignment_date': get_date_time_str(self.assignment_date),
            'unlock_date': get_date_time_str(self.unlock_date)
        }

    def __str__(self):
        return f'Assigment({self.id}, {self.name}, {self.group_id}, {self.course_section_id}, {self.points}, {get_date_time_str(self.assignment_date)})'

    @staticmethod
    def from_dict(data_dict):
        if 'unlock_date' in data_dict:
            return Assignment(data_dict['id'], data_dict['name'], data_dict['group_id'], data_dict['course_section_id'],
                              data_dict['points'],
                              get_date_time_obj(data_dict['assignment_date']),
                              get_date_time_obj(data_dict['unlock_date']))
        else:

            return Assignment(data_dict['id'], data_dict['name'], data_dict['group_id'], data_dict['course_section_id'],
                              data_dict['points'],
                              get_date_time_obj(data_dict['assignment_date']), get_date_time_obj("2023-02-06T00:00:00Z"))

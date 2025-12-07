BEFORE_DEADLINE = "1"
NOT_YET_GRADED = "2"
NOT_CORRECT_GRADED = "3"
MISSED_ITEM = "4"
GRADED = "5"


class Status:
    def __init__(self, label, color):
        self.label = label
        self.color = color

    def to_json(self):
        return {
            'label': self.label,
            'color': self.color
        }

    def __str__(self):
        return f'Status({self.label}, {self.color})'

    @staticmethod
    def from_dict(data_dict):
        level = Status(data_dict['label'], data_dict['color'])
        return level


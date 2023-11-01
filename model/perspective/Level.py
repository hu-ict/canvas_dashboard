class Level:
    def __init__(self, label, color):
        self.label = label
        self.color = color

    def to_json(self):
        return {
            'label': self.label,
            'color': self.color
        }

    def __str__(self):
        return f'Level({self.label}, {self.color})'

    @staticmethod
    def from_dict(data_dict):
        return Level(data_dict['label'], data_dict['color'])


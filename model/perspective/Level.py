class Level:
    def __init__(self, label, color):
        self.label = label
        self.color = color
        self.fraction = 0
        self.value = 0

    def to_json(self):
        return {
            'label': self.label,
            'color': self.color
        }

    def __str__(self):
        return f'Level({self.label}, {self.color})'

    @staticmethod
    def from_dict(data_dict):
        level = Level(data_dict['label'], data_dict['color'])
        if 'fraction' in data_dict.keys():
            level.fraction = data_dict['fraction']
        return level


class Level:
    def __init__(self, level, label, color, fraction, value):
        self.level = level
        self.label = label
        self.color = color
        self.fraction = fraction
        self.value = value

    def to_json(self):
        return {
            'label': self.label,
            'color': self.color,
            'fraction': self.fraction,
            'value': self.value
        }

    def __str__(self):
        return f'Level({self.level}, {self.label}, {self.color}, {self.fraction}, {self.value})'

    @staticmethod
    def from_dict(data_dict):
        print("LE01 -", data_dict)
        if 'fraction' in data_dict:
            level = Level(data_dict['level'], data_dict['label'], data_dict['color'], data_dict['fraction'], data_dict['value'])
        else:
            level = Level(data_dict['label'], data_dict['color'], 0, 0)
        return level


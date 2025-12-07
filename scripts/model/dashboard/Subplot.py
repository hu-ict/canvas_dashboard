class Subplot:
    def __init__(self, rows, cols, titles, positions, specs):
        self.rows = rows
        self.cols = cols
        self.titles = titles
        self.positions = positions
        self.specs = specs

    def to_json(self):
        return {
            'rows': self.rows,
            'cols': self.cols,
            'titles': self.titles,
            'positions': self.positions,
            'specs': self.specs
        }

    @staticmethod
    def from_dict(data_dict):
        new = Subplot(data_dict["rows"], data_dict["cols"], data_dict["titles"], data_dict["positions"],data_dict["specs"])
        return new

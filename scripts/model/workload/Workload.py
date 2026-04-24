class Workload:
    def __init__(self, day):
        self.day = day
        self.dimensions = []

    # def to_json(self):
    #     return {
    #         'day': self.day,
    #         'workload_dimensions': self.workload_dimensions,
    #
    #     }

    def __str__(self):
        return f'Workload{self.day}, {self.dimensions})\n'

    def get_dimension(self, name):
        for dimension in self.dimensions:
            if dimension.name == name:
                return dimension
        return None
    #
    # @staticmethod
    # def from_dict(data_dict):
    #     new = Workload(data_dict['day'])
    #     new.workload_dimensions = data_dict['workload_dimensions']
    #     return new


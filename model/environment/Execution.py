class Execution:
    def __init__(self, name, source_path, target_path):
        self.name = name
        self.source_path = source_path
        self.target_path = target_path

    def __str__(self):
        return f'Action({self.name}, {self.source_path}, {self.target_path})'

    def to_json(self):
        dict_result = {
            'name': self.name,
            'source_path': self.source_path,
            'target_path': self.target_path
        }
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        # print(data_dict)
        new = Execution(data_dict['name'], data_dict['source_path'], data_dict['target_path'])
        return new

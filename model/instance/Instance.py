from model.instance.Action import Action


class Instance:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.listen = {}


    def to_json(self):
        dict_result = {
            'name': self.name,
            'category': self.category,
            'listen': {}
        }
        for key in self.listen:
            dict_result['listen'][key] = self.listen[key].to_json()
        return dict_result

    def __str__(self):
        line = f' Instance({self.name}, {self.category})\n'
        for key in self.listen.keys():
            line += f'{self.listen[key]}\n'
        return line

    @staticmethod
    def from_dict(key, data_dict):
        # print(data_dict)
        new = Instance(data_dict["name"], data_dict["category"])
        for key in data_dict["listen"].keys():
            new.listen[key] = Action.from_dict(key, data_dict["listen"][key])
        return new

class Event:
    def __init__(self, name, trigger):
        self.name = name
        self.trigger = trigger

    def __str__(self):
        return f' Event({self.name}, {self.trigger})\n'


    @staticmethod
    def from_dict(key, data_dict):
        # print(data_dict)
        new = Event(data_dict['name'], data_dict['trigger'])
        return new
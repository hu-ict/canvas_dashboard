class WorkloadDimension:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []

    def to_json(self):
        return {
            'name': self.name,
            'items': self.items
        }

    def __str__(self):
        return f'WorkloadDimension {self.name} {self.items})\n'

    def get_workload_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def get_shorts(self):
        shorts = []
        for item in self.items:
            shorts.append(item.short)
        return shorts

    def get_w1_count(self):
        w1_count = []
        for item in self.items:
            w1_count.append(item.w1_count)
        return w1_count

    def get_w2_count(self):
        w2_count = []
        for item in self.items:
            w2_count.append(item.w2_count)
        return w2_count

    def get_w3_count(self):
        w3_count = []
        for item in self.items:
            w3_count.append(item.w3_count)
        return w3_count

    @staticmethod
    def from_dict(data_dict):
        new = WorkloadDimension(data_dict['name'])
        new.items = data_dict['items']
        return new


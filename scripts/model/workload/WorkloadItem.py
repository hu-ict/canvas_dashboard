class WorkloadItem:
    def __init__(self, id, short, name, bof_count, total_value, w1_count, w2_count, w3_count):
        self.item_id = id
        self.short = short
        self.name = name
        self.w1_count = w1_count
        self.w2_count = w2_count
        self.w3_count = w3_count
        self.total_value = total_value
        self.bof_count = bof_count
        self.worklist = []

    def to_json(self):
        return {
            'item_id': self.item_id,
            'short': self.short,
            'name': self.name,
            'bof_count':self.bof_count,
            'total_value': self.total_value,
            'w1_count': self.w1_count,
            'w2_count': self.w2_count,
            'w3_count': self.w3_count,
            'worklist': self.worklist
        }

    def __str__(self):
        return f'WorkloadDay({self.item_id}, {self.short}, {self.name}, {self.worklist})'

    @staticmethod
    def from_dict(data_dict):
        new = WorkloadItem(data_dict['item_id'], data_dict['short'], data_dict['name'], 0, 0, data_dict['w1_count'], data_dict['w2_count'], data_dict['w3_count'])
        if 'bof_count' in data_dict:
            new.bof_value_quotient = data_dict['bof_count']
        if 'total_value' in data_dict:
            new.bof_value_quotient = data_dict['total_value']
        new.work_list = data_dict['worklist']
        return new


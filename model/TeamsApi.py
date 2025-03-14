class Channel:
    def __init__(self, a_student_id, a_name, a_channel):
        self.id = a_student_id
        self.name = a_name
        self.channel = a_channel

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'channel': self.channel
        }

    def __str__(self):
        return f'Channel({self.id}, {self.name}, {self.channel})'

    @staticmethod
    def from_dict(data_dict):
        # print("Student.from_dict", data_dict)
        return Channel(data_dict['id'], data_dict['name'], data_dict['channel'])


class TeamsApi:
    def __init__(self, a_tenant_id, a_tenant_name, a_client_id, a_gen_token, a_my_token):
        self.tenant_id = a_tenant_id
        self.tenant_name = a_tenant_name
        self.client_id = a_client_id
        self.gen_token = a_gen_token
        self.my_token = a_my_token
        self.channels = []

    def to_json(self):
        return {'tenant_id': self.tenant_id, 'tenant_name': self.tenant_name, 'client_id': self.client_id,
                       'gen_token': self.gen_token, 'my_token': self.my_token,
                       'channels': list(map(lambda c: c.to_json(), self.channels))}

    def __str__(self):
        return f'TeamsApi({self.tenant_id}, {self.tenant_name}, {self.client_id}, {self.gen_token}, {self.my_token}'

    @staticmethod
    def from_dict(data_dict):
        new = TeamsApi(data_dict['tenant_id'], data_dict['tenant_name'], data_dict['client_id'],
                       data_dict['gen_token'], data_dict['my_token'])
        new.channels = list(map(lambda s: Channel.from_dict(s), data_dict['channels']))
        return new

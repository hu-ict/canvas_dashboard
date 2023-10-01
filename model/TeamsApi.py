class TeamsApi:
    def __init__(self, a_tenant_id, a_tenant_name, a_client_id, a_gen_token, a_my_token):
        self.tenant_id = a_tenant_id
        self.tenant_name = a_tenant_name
        self.client_id = a_client_id
        self.gen_token = a_gen_token
        self.my_token = a_my_token

    def to_json(self):
        return {
            'tenant_id': self.tennant_id,
            'tenant_name': self.tennant_name,
            'client_id': self.client_id,
            'gen_token': self.gen_token,
            'my_token': self.my_token
        }

    def __str__(self):
        return f'TeamsApi({self.tenant_id}, {self.tenant_name}, {self.client_id}, {self.gen_token}, {self.my_token}'

    @staticmethod
    def from_dict(data_dict):
        new = TeamsApi(data_dict['tenant_id'], data_dict['tenant_name'], data_dict['client_id'], data_dict['gen_token'], data_dict['my_token'])
        return new

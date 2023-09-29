class TeamsApi:
    def __init__(self, a_tennant_id, a_token):
        self.tennant_id = a_tennant_id
        self.token = a_token

    def to_json(self):
        return {
            'tennant_id': self.tennant_id,
            'token': self.token
        }

    def __str__(self):
        return f'TeamsApi({self.tennant_id}, {self.token}'

    @staticmethod
    def from_dict(data_dict):
        new_teacher = TeamsApi(data_dict['tennant_id'], data_dict['token'])
        return new_teacher

class SecretApiKey:
    def __init__(self, name, canvas_api_key):
        self.name = name
        self.canvas_api_key = canvas_api_key

    def to_json(self):
        return {'name': self.name, 'canvas_api_key': self.canvas_api_key}

    def __str__(self):
        return f'SecretApiKey({self.name})'

    @staticmethod
    def from_dict(data_dict):
        new = SecretApiKey(data_dict["name"], data_dict['canvas_api_key'])
        return new

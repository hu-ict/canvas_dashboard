class Page:
    def __init__(self, page_id, name, url):
        self.id = page_id
        self.name = name
        self.url = url
        self.is_in_module = False

    def to_json(self, scope):
        return {
            'name': self.name,
            'id': self.id,
            'url': self.url,
            'is_in_module': self.is_in_module
        }

    def __str__(self):
        line = f'Page({self.id}, {self.name}, {self.url})'
        return line

    @staticmethod
    def from_dict(data_dict):
        new_student = Page(data_dict['id'],data_dict['name'],data_dict['url'])
        new_student.is_in_module = data_dict['is_in_module']
        return new_student

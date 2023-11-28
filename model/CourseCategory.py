class CourseCatergory:
    def __init__(self, category, course_instances):
        self.category = category
        self.course_instances = course_instances

    def to_json(self):
        dict_result = {
            'category': self.category,
            'course_instances': self.course_instances
        }
        return dict_result

    def __str__(self):
        line = f'CourseCatergory({self.category}, {self.course_instances})'
        return line

    @staticmethod
    def from_dict(key, data_dict):
        # print("CourseCatergory", key, data_dict)
        new = CourseCatergory(key, data_dict)
        return new
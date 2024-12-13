class CourseCategory:
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
        line = f' CourseCategory({self.category}, {self.course_instances})\n'
        return line

    @staticmethod
    def from_dict(key, data_dict):
        # print("CourseCategory", key, data_dict)
        new = CourseCategory(key, data_dict['course_instances'])
        return new
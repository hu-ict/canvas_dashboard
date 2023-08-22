from model.Submission import Submission


class Perspective:
    def __init__(self, name):
        self.name = name
        self.assignment_groups = []

    def to_json(self):
        return {
            'name': self.name,
            'assignment_groups': self.assignment_groups,
        }

    def __str__(self):
        line = f' Perspective({self.name}, {self.assignment_groups})\n'
        return line

    # def get_submission_by_assignment(self, assigment_id):
    #     for submission in self.submissions:
    #         if submission.assignment_id == assigment_id:
    #             return submission
    #     return None
    #
    # def put_submission(self, a_submission):
    #     index = -1
    #     for i in range(len(self.submissions)):
    #         if self.submissions[i].id == a_submission.id:
    #             index = i
    #             break
    #     if index >= 0:
    #         self.submissions[index] = a_submission
    #     else:
    #         self.submissions.append(a_submission)
    #     return

    @staticmethod
    def from_dict(data_dict):
        new_perspective = Perspective(data_dict['name'])
        if 'assignment_groups' in data_dict.keys():
            new_perspective.assignment_groups = data_dict['assignment_groups']
        return new_perspective

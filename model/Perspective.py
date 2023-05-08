from model.Submission import Submission


class Perspective:
    def __init__(self, name):
        self.name = name
        self.assignment_groups = []
        self.submissions = []

    def to_json(self):
        return {
            'name': self.name,
            'assignment_groups': self.assignment_groups,
            'submissions': list(map(lambda s: s.to_json(), self.submissions))
        }

    def __str__(self):
        line = f' Perspective({self.name}, {self.assignment_groups}, {self.submissions})\n'
        for submission in self.submissions:
            line += " p " + str(submission)+ "\n"
        return line

    def get_submission(self, assigment_id):
        for submission in self.submissions:
            if submission.assignment_id == assigment_id:
                return submission
        return None

    @staticmethod
    def from_dict(data_dict):
        new_perspective = Perspective(data_dict['name'])
        new_perspective.assignment_groups = data_dict['assignment_groups']
        new_perspective.submissions = list(map(lambda s: Submission.from_dict(s), data_dict['submissions']))
        return new_perspective

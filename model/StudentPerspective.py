from model.Submission import Submission


class StudentPerspective:
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
        line = f' StudentPerspective({self.name}, {self.assignment_groups})\n'
        for submission in self.submissions:
            line += " s " + str(submission) + "\n"
        return line

    def get_submission_by_assignment(self, assigment_id):
        for submission in self.submissions:
            if submission.assignment_id == assigment_id:
                return submission
        return None

    def put_submission(self, a_submission):
        index = -1
        for i in range(len(self.submissions)):
            if self.submissions[i].id == a_submission.id:
                index = i
                break
        if index >= 0:
            self.submissions[index] = a_submission
        else:
            self.submissions.append(a_submission)
        return

    @staticmethod
    def from_dict(data_dict):
        new_perspective = StudentPerspective(data_dict['name'])
        if 'assignment_groups' in data_dict.keys():
            new_perspective.assignment_groups = data_dict['assignment_groups']
        if 'submissions' in data_dict.keys():
            new_perspective.submissions = list(map(lambda s: Submission.from_dict(s), data_dict['submissions']))
        return new_perspective

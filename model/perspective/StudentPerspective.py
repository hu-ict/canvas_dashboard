from model.Submission import Submission


class StudentPerspective:
    def __init__(self, name, progress, sum_score, last_score):
        self.name = name
        self.progress = progress
        self.sum_score = sum_score
        self.last_score = last_score
        self.assignment_groups = []
        self.submissions = []

    def to_json(self):
        return {
            'name': self.name,
            'progress': self.progress,
            'sum_score': self.sum_score,
            'last_score': self.last_score,
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
            # Als de Submission bestaat wordt deze overschreven met de nieuwe versie
            self.submissions[index] = a_submission
        else:
            # Als de Submission niet bestaat, dan wordt deze aan de lijst toegevoegd
            self.submissions.append(a_submission)
        return

    @staticmethod
    def from_dict(data_dict):
        # print("StudentPerspective.from_dict", data_dict)
        if 'last_score' in data_dict.keys():
            new = StudentPerspective(data_dict['name'], data_dict['progress'], data_dict['sum_score'], data_dict['last_score'])
        else:
            new = StudentPerspective(data_dict['name'], 0, 0, 0)
        if 'assignment_groups' in data_dict.keys():
            new.assignment_groups = data_dict['assignment_groups']
        if 'submissions' in data_dict.keys():
            new.submissions = list(map(lambda s: Submission.from_dict(s), data_dict['submissions']))
        return new

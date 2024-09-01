from model.Assignment import Assignment
from model.Submission import Submission


class SubmissionSequence:
    def __init__(self, name, tag, grading_type, points, flow):
        self.name = name
        self.tag = tag
        self.grading_type = grading_type
        self.points = points
        self.flow = flow
        self.submissions = []


    def __str__(self):
        return f'SubmissionSequence({self.name}, {self.tag}, {self.grading_type}, {self.points})'

    def get_day(self):
        if len(self.submissions) > 0:
            return self.get_actual_submission().assignment_day
        return None

    def get_score(self):
        '''
        Look for the highest score
        '''
        score = 0
        for submission in self.submissions:
            if submission.score > score:
                score = submission.score
        return score

    def is_graded(self):
        for submission in self.submissions:
            if submission.graded:
                return True
        return False

    def get_actual_submission(self):
        '''
        Find de submission with the highest score
        '''
        score = -1
        actual_submission = None
        for submission in self.submissions:
            if submission.score > score:
                score = submission.score
                actual_submission = submission
        return actual_submission

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


    def to_json(self):
        return {
            'name': self.name,
            'tag': self.tag,
            'grading_type': self.grading_type,
            'points': int(self.points),
            'flow': round(self.flow, 2),
            'submissions': list(map(lambda a: a.to_json(), self.submissions)),
        }

    @staticmethod
    def from_dict(data_dict):
        new = SubmissionSequence(data_dict['name'], data_dict['tag'], data_dict['grading_type'], data_dict['points'], data_dict['flow'])
        if 'submissions' in data_dict.keys():
            new.submissions = list(map(lambda a: Submission.from_dict(a), data_dict['submissions']))
        return new

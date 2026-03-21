from scripts.lib.lib_date import get_date_time_obj, get_date_time_str
from scripts.lib.lib_portfolio import STATUS_MISSED, STATUS_PENDING, STATUS_COMPLETE, STATUS_INCOMPLETE
from scripts.model.Comment import Comment
from scripts.model.SubmissionAssignment import SubmissionAssignment
from scripts.model.rubric.CriteriumScore import CriteriumScore
from scripts.model.perspective.Status import NOT_CORRECT_GRADED, NOT_YET_GRADED, GRADED, MISSED_ITEM, BEFORE_DEADLINE


class Submission:
    def __init__(self, submission_id, submission_assignment, student_id,
                 submitted_date, submitted_day,
                 status, graded, posted,
                 grade, grader_id, grader_name, graded_date,
                 score, value, flow):
        self.id = submission_id
        self.assignment = submission_assignment
        self.student_id = student_id
        self.submitted_date = submitted_date
        self.submitted_day = submitted_day
        self.status = status
        self.graded = graded
        self.posted = posted
        self.grade = grade
        self.grader_id = grader_id
        self.grader_name = grader_name
        self.graded_date = graded_date
        self.score = score
        self.value = value
        self.flow = flow
        self.body = None
        self.messages = []
        self.comments = []
        self.rubrics = []

    def to_json(self):
        if self.flow is None:
            l_flow = None
        else:
            l_flow = int(self.flow*10)/10
        if self.score is None:
            l_score = None
        else:
            l_score = int(self.score*10)/10
        if self.value is None:
            l_value = None
        else:
            l_value = int(self.value * 10) / 10
        return {
            'id': self.id,
            'student_id': self.student_id,
            'status': self.status,
            'assignment': self.assignment.to_json(),
            'submitted_date': get_date_time_str(self.submitted_date),
            'submitted_day': self.submitted_day,
            'graded': self.graded,
            'posted': self.posted,
            'grade': self.grade,
            'grader_id': self.grader_id,
            'grader_name': self.grader_name,
            "graded_date": get_date_time_str(self.graded_date),
            'score': l_score,
            'value': l_value,
            'flow': l_flow,
            'body': self.body,
            'messages': self.messages,
            'comments': list(map(lambda c: c.to_json(), self.comments)),
            'rubrics': list(map(lambda r: r.to_json(), self.rubrics)),
        }

    def get_criterium_score(self, criterium_id):
        for criterium in self.rubrics:
            if criterium.id == criterium_id:
                return criterium
        return None

    def get_status(self):
        if self.status == NOT_CORRECT_GRADED:
            return NOT_CORRECT_GRADED
        if self.status == NOT_YET_GRADED:
            return NOT_YET_GRADED
        if self.graded:
            return GRADED
        if self.score == 0:
            return MISSED_ITEM
        return BEFORE_DEADLINE

    def get_complete_status_css(self):
        if self.get_status() == GRADED:
            if self.graded and self.score == self.assignment.points:
                return STATUS_COMPLETE
            return STATUS_INCOMPLETE
        else:
            if self.status is MISSED_ITEM:
                return STATUS_MISSED
            else:
                return STATUS_PENDING
        return "status_unknown"

    def __str__(self):
        return f'Submission({self.id}, {self.student_id}, ' \
               f'{get_date_time_str(self.submitted_date)}, {self.graded}, {self.status}, ' \
               f'{self.score}, {self.value}, Comments: {len(self.comments)})'

    @staticmethod
    def from_dict(data_dict):
        new_submission = Submission(data_dict['id'], SubmissionAssignment.from_dict(data_dict['assignment']), data_dict['student_id'],
                                    get_date_time_obj(data_dict['submitted_date']), data_dict['submitted_day'],
                                    data_dict['status'], data_dict['graded'], data_dict['posted'],
                                    data_dict['grade'], data_dict['grader_id'], data_dict['grader_name'],
                                    get_date_time_obj(data_dict['graded_date']), data_dict['score'],
                                    data_dict['value'], data_dict['flow'])
        new_submission.comments = list(map(lambda c: Comment.from_dict(c), data_dict['comments']))
        new_submission.rubrics = list(map(lambda c: CriteriumScore.from_dict(c), data_dict['rubrics']))
        # print("SU05 -", data_dict)
        if ("body" in data_dict) and (data_dict['body'] is not None) and len(data_dict['body']) > 0:
            new_submission.body = data_dict['body']
        if ("messages" in data_dict) and (data_dict['messages'] is not None) and len(data_dict['messages']) > 0:
            new_submission.messages = data_dict['messages']
        return new_submission


from lib.lib_date import get_date_time_obj, get_date_time_str
from model.Comment import Comment
from model.CriteriumScore import CriteriumScore
from model.perspective.Status import NOT_CORRECT_GRADED, NOT_YET_GRADED, GRADED, MISSED_ITEM, BEFORE_DEADLINE


class Submission:
    def __init__(self, submission_id, assignment_group_id, assignment_id, student_id,
                 assignment_name, assignment_date, assignment_day,
                 submitted_date, submitted_day,
                 status, graded,
                 grade, grader_name, graded_date,
                 score, value, points, flow):
        self.id = submission_id
        self.assignment_group_id = assignment_group_id
        self.assignment_name = assignment_name
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.assignment_date = assignment_date
        self.assignment_day = assignment_day
        self.submitted_date = submitted_date
        self.submitted_day = submitted_day
        self.status = status
        self.graded = graded
        self.grade = grade
        self.grader_name = grader_name
        self.graded_date = graded_date
        self.score = score
        self.value = value
        self.points = points
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
            'assignment_group_id': self.assignment_group_id,
            'assignment_id': self.assignment_id,
            'student_id': self.student_id,
            'assignment_name': self.assignment_name,
            'assignment_date': get_date_time_str(self.assignment_date),
            'assignment_day': self.assignment_day,
            'submitted_date': get_date_time_str(self.submitted_date),
            'submitted_day': self.submitted_day,
            'status': self.status,
            'graded': self.graded,
            'grade': self.grade,
            'grader_name': self.grader_name,
            "graded_date": get_date_time_str(self.graded_date),
            'score': l_score,
            'value': l_value,
            'points': int(self.points),
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
            if self.graded and self.score == self.points:
                return "status_complete"
            return "status_incomplete"
        else:
            if self.status is MISSED_ITEM:
                return "status_missed"
            else:
                return "status_pending"
        return "status_unknown"

    def __str__(self):
        return f'Submission({self.id}, {self.assignment_group_id}, {self.assignment_id}, {self.student_id}, ' \
               f'{self.assignment_name}, {get_date_time_str(self.assignment_date)}, ' \
               f'{get_date_time_str(self.submitted_date)}, {self.graded}, {self.status}, ' \
               f'{self.score}, {self.value}, {self.points}, Comments: {len(self.comments)})'

    @staticmethod
    def from_dict(data_dict):
        new_submission = Submission(data_dict['id'], data_dict['assignment_group_id'], data_dict['assignment_id'],
                                    data_dict['student_id'], data_dict['assignment_name'],
                                    get_date_time_obj(data_dict['assignment_date']), data_dict['assignment_day'],
                                    get_date_time_obj(data_dict['submitted_date']), data_dict['submitted_day'],
                                    data_dict['status'],
                                    data_dict['graded'], data_dict['grade'], data_dict['grader_name'],
                                    get_date_time_obj(data_dict['graded_date']), data_dict['score'],
                                    data_dict['value'], data_dict['points'], data_dict['flow'])
        new_submission.comments = list(map(lambda c: Comment.from_dict(c), data_dict['comments']))
        new_submission.rubrics = list(map(lambda c: CriteriumScore.from_dict(c), data_dict['rubrics']))
        # print("SU05 -", data_dict)
        if ("body" in data_dict) and (data_dict['body'] is not None) and len(data_dict['body']) > 0:
            new_submission.body = data_dict['body']
        if ("messages" in data_dict) and (data_dict['messages'] is not None) and len(data_dict['messages']) > 0:
            new_submission.messages = data_dict['messages']
        return new_submission


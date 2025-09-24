from model.SubmissionSequence import SubmissionSequence


class StudentPerspective:
    def __init__(self, name, title, progress, sum_score, last_score):
        self.name = name
        self.title = title
        self.progress = progress
        self.sum_score = sum_score
        self.last_score = last_score
        self.assignment_group_ids = []
        self.submission_sequences = []

    def to_json(self):
        return {
            'name': self.name,
            'title': self.title,
            'progress': self.progress,
            'sum_score': self.sum_score,
            'last_score': self.last_score,
            'assignment_group_ids': self.assignment_group_ids,
            'submission_sequences': list(map(lambda s: s.to_json(), self.submission_sequences))
        }

    def __str__(self):
        line = f' StudentPerspective({self.name}, {self.assignment_group_ids})\n'
        for submission_sequence in self.submission_sequences:
            line += " s " + str(submission_sequence) + "\n"
        return line

    def get_sequence_by_tag(self, tag):
        for submission_sequence in self.submission_sequences:
            if submission_sequence.tag == tag:
                return submission_sequence
        return None

    def get_submission_by_assignment(self, assigment_id):
        for submission_sequence in self.submission_sequences:
            for submission in submission_sequence.submissions:
                if submission.assignment_id == assigment_id:
                    return submission
        return None

    # def get_submission_sequence_by_assignment_id(self, assignment_id):
    #     for submission_sequence in self.submission_sequences:
    #         for submission in submission_sequence.submissions:
    #             # print(submission_sequence.name, submission.assignment_name, submission.assignment_id, assignment_id)
    #             if int(submission.assignment_id) == int(assignment_id):
    #                 return submission_sequence
    #     return None

    def get_submission_sequence_by_tag(self, tag):
        for submission_sequence in self.submission_sequences:
            if submission_sequence.tag == tag:
                return submission_sequence
        return None

    def get_submitted(self, assignment_sequence, actual_day):
        passed_assignments = assignment_sequence.get_passed_assignments(actual_day)
        if len(passed_assignments) > 0:
            submission_sequence = self.get_submission_sequence_by_tag(assignment_sequence.tag)
            if submission_sequence is None:
                # geen submission
                return None
            if len(submission_sequence.submissions) == 0:
                # geen submission
                return None
            submission = submission_sequence.get_actual_submission()
            return submission
        else:
            return None

    def put_submission(self, a_assignment_sequence, a_submission):
        submission_sequence = self.get_submission_sequence_by_tag(a_assignment_sequence.tag)
        if submission_sequence is None:
            submission_sequence = SubmissionSequence(a_assignment_sequence.name, a_assignment_sequence.tag,
                                                     a_assignment_sequence.grading_type,
                                                     a_assignment_sequence.points, 0)
            self.submission_sequences.append(submission_sequence)
        submission_sequence.put_submission(a_submission)
        return

    @staticmethod
    def from_dict(data_dict):
        # print("StudentPerspective.from_dict", data_dict)
        if 'last_score' in data_dict.keys():
            new = StudentPerspective(data_dict['name'], data_dict['title'], data_dict['progress'],
                                     data_dict['sum_score'], data_dict['last_score'])
        else:
            new = StudentPerspective(data_dict['name'], data_dict['title'], 0, 0, 0)
        if 'assignment_group_ids' in data_dict.keys():
            new.assignment_group_ids = data_dict['assignment_group_ids']
        if 'submission_sequences' in data_dict.keys():
            new.submission_sequences = list(map(lambda s: SubmissionSequence.from_dict(s),
                                                data_dict['submission_sequences']))
        return new

    @staticmethod
    def copy_from(course, student, perspective):
        new = StudentPerspective(perspective.name, perspective.title, -1, 0, 0)
        if len(perspective.assignment_group_ids) > 1:
            new.assignment_group_ids.append(course.find_assignment_group_by_role(student.role))
        else:
            new.assignment_group_ids = perspective.assignment_group_ids
        return new

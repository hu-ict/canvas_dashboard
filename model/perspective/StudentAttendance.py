from model.perspective.AttendanceSubmission import AttendanceSubmission


class StudentAttendance:
    def __init__(self, name, progress, count, percentage, essential_count, essential_percentage, last_score):
        self.name = name
        self.progress = progress
        self.count = count
        self.percentage = percentage
        self.essential_count = essential_count
        self.essential_percentage = essential_percentage
        self.last_score = last_score
        self.attendance_submissions = []

    def to_json(self):
        return {
            'name': self.name,
            'progress': self.progress,
            'count': self.count,
            'percentage': self.percentage,
            'essential_count': self.essential_count,
            'essential_percentage': self.essential_percentage,
            'last_score': self.last_score,
            'attendance_submissions': list(map(lambda s: s.to_json(), self.attendance_submissions))
        }

    def __str__(self):
        lines = f'AttendancePerspective({self.name} progress {self.progress}, count {self.count}, ' \
                f'percentage {self.percentage}, essential_count {self.essential_count}, ' \
                f'essential_percentage {self.essential_percentage}, last_score {self.last_score})'
        for attendance_submission in self.attendance_submissions:
            lines += "\n s " + str(attendance_submission)
        return lines

    # def put_submission(self, a_submission):
    #     index = -1
    #     for i in range(len(self.attendance_submissions)):
    #         if self.submissions[i].id == a_submission.id:
    #             index = i
    #             break
    #     if index >= 0:
    #         # Als de Submission bestaat wordt deze overschreven met de nieuwe versie
    #         self.attendance_submissions[index] = a_submission
    #     else:
    #         # Als de Submission niet bestaat, dan wordt deze aan de lijst toegevoegd
    #         self.attendance_submissions.append(a_submission)
    #     return

    @staticmethod
    def from_dict(data_dict):
        # print("StudentPerspective.from_dict", data_dict)
        if 'count' in data_dict.keys():
            new = StudentAttendance(data_dict['name'], data_dict['progress'], data_dict['count'],
                                    data_dict['percentage'], data_dict['essential_count'],
                                    data_dict['essential_percentage'], data_dict['last_score'])
        else:
            new = StudentAttendance(data_dict['name'], -1, 0, 0, 0, 0, 0)
        if 'attendance_submissions' in data_dict.keys():
            new.attendance_submissions = list(
                map(lambda s: AttendanceSubmission.from_dict(s), data_dict['attendance_submissions']))
        return new

    @staticmethod
    def copy_from(attendance):
        return StudentAttendance(attendance.name, -1, 0, 0, 0, 0, 0)

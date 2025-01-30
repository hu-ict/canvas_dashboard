from model.perspective.StudentAttendance import StudentAttendance
from model.perspective.StudentGradeMoments import StudentGradeMoments
from model.perspective.StudentLevelMoments import StudentLevelMoments
from model.perspective.StudentPerspective import StudentPerspective


class StudentResults:
    def __init__(self, a_student_id, a_group_id, a_name, a_number, a_sortable_name, a_coach, a_role, a_email, a_site,
                 a_progress):
        self.id = a_student_id
        self.group_id = a_group_id
        self.name = a_name
        self.number = a_number
        self.sortable_name = a_sortable_name
        self.coach = a_coach
        self.email = a_email
        self.site = a_site
        self.progress = a_progress
        self.role = a_role
        self.student_level_moments = None
        self.student_grade_moments = None
        self.student_attendance = None
        self.perspectives = {}

    def __str__(self):
        line = f'StudentResults({self.id}, {self.group_id}, {self.name}, {self.number}, {self.coach}, {self.role}, {self.email}, {self.progress})\n'
        if self.perspectives is not None:
            for perspective in self.perspectives:
                line += " p "+str(self.perspectives[perspective])
        line += " a "+str(self.attendance_perspective)
        return line

    def get_perspective(self, name):
        for perspective in self.perspectives:
            if perspective.name == name:
                return perspective
        return None

    def get_submission_sequence_by_name(self, name):
        for student_perspective in self.perspectives.values():
            for submission_sequence in student_perspective.submission_sequences:
                if submission_sequence.name == name:
                    return submission_sequence
        return None

    def to_json(self):
        dict_result = {
            'name': self.name,
            'id': self.id,
            'number': self.number,
            'sortable_name': self.sortable_name,
            'group_id': self.group_id,
            'coach': self.coach,
            'email': self.email,
            'site': self.site,
            'role': self.role,
            'progress': self.progress,
            'perspectives': {}
        }
        if self.student_level_moments is not None:
            dict_result['student_level_moments'] = self.student_level_moments.to_json()
        if self.student_grade_moments is not None:
            dict_result['student_grade_moments'] = self.student_grade_moments.to_json()
        if self.student_attendance is not None:
            dict_result['student_attendance'] = self.student_attendance.to_json()
        for key in self.perspectives:
            dict_result['perspectives'][key] = self.perspectives[key].to_json()
        return dict_result

    def get_perspective(self, name):
        for perspective in self.perspectives:
            if perspective.name == name:
                return perspective
        return None

    def get_level_moment(self, assigment_id):
        for peilmoment in self.student_level_moments.submissions:
            if peilmoment.assignment_id == assigment_id:
                return peilmoment
        return None

    def get_level_moment_submission_by_query(self, a_query):
        for submission in self.student_level_moments.submissions:
            condition = 0
            for selector in a_query:
                if selector.lower() in submission.assignment_name.lower():
                    condition += 1
            if condition == len(a_query):
                return submission
        return None

    def get_level_moment_submissions_by_query(self, a_query):
        submissions = []
        for submission in self.student_level_moments.submissions:
            condition = 0
            for selector in a_query:
                if selector.lower() in submission.assignment_name.lower():
                    condition += 1
            if condition == len(a_query):
                submissions.append(submission)
        return submissions

    def get_grade_moment(self, assigment_id):
        for grade_moment in self.student_grade_moments.submissions:
            if grade_moment.assignment_id == assigment_id:
                return grade_moment
        return None

    def get_grade_moment_submission_by_query(self, a_query):
        for grade_moment in self.student_grade_moments.submissions:
            condition = 0
            for selector in a_query:
                if selector.lower() in grade_moment.assignment_name.lower():
                    condition += 1
            if condition == len(a_query):
                return grade_moment
        return None

    def get_grade_moment_submissions_by_query(self, a_query):
        grade_moments = []
        for grade_moment in self.student_grade_moments.submissions:
            condition = 0
            # moet aan alle selectie criteria voldoen
            for selector in a_query:
                if selector.lower() in grade_moment.assignment_name.lower():
                    condition += 1
            if condition == len(a_query):
                grade_moments.append(grade_moment)
        return grade_moments

    # def get_judgement(self, perspective_name):
    #     for level_moment in self.student_level_moments.submissions:
    #         if perspective_name in level_moment.assignment_name.lower() and "beoordeling" in level_moment.assignment_name.lower():
    #             return int(level_moment.score)
    #     return None

    def get_submission_sequence_by_name(self, name):
        for student_perspective in self.perspectives.values():
            for submission_sequence in student_perspective.submission_sequences:
                if submission_sequence.name == name:
                    return submission_sequence
        return None


    @staticmethod
    def from_dict(data_dict):
        # print("Student.from_dict", data_dict)
        if 'number' in data_dict.keys():
            new = StudentResults(data_dict['id'], data_dict['group_id'], data_dict['name'], data_dict['number'],
                                 data_dict['sortable_name'], data_dict['coach'], data_dict['role'], data_dict['email'],
                                 data_dict[ 'site'], data_dict['progress'])
        else:
            new = StudentResults(data_dict['id'], data_dict['group_id'], data_dict['name'], "x",
                                 data_dict['sortable_name'], data_dict['coach'], data_dict['role'], data_dict['email'],
                                 data_dict[ 'site'], data_dict['progress'])

        if 'student_level_moments' in data_dict.keys() and data_dict['student_level_moments'] is not None:
            new.student_level_moments = StudentLevelMoments.from_dict(data_dict['student_level_moments'])
            # print("SR41 -", new.student_level_moments)
        if 'student_grade_moments' in data_dict.keys() and data_dict['student_grade_moments'] is not None:
            new.student_grade_moments = StudentGradeMoments.from_dict(data_dict['student_grade_moments'])
        if 'student_attendance' in data_dict.keys() and data_dict['student_attendance'] is not None:
            new.student_attendance = StudentAttendance.from_dict(data_dict['student_attendance'])
        for key in data_dict['perspectives'].keys():
            new.perspectives[key] = StudentPerspective.from_dict(data_dict['perspectives'][key])
        return new

    @staticmethod
    def copy_from(student, course):
        # print("Student.from_dict", data_dict)
        new = StudentResults(student.id, student.group_id, student.name, student.number, student.sortable_name,
                             student.coach, student.role, student.email, student.site, -1)
        for perspective in course.perspectives.values():
            new.perspectives[perspective.name] = StudentPerspective.copy_from(course, student, perspective)
        if course.level_moments is not None:
            new.student_level_moments = StudentLevelMoments.copy_from(course.level_moments)
        if course.grade_moments is not None:
            new.student_grade_moments = StudentGradeMoments.copy_from(course.grade_moments)
        if course.attendance is not None:
            new.student_attendance = StudentAttendance.copy_from(course.attendance)
        return new


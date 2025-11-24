from model.Submission import Submission
from model.moment.StudentMomentsBase import StudentMomentsBase


class StudentGradeMoments(StudentMomentsBase):
    @staticmethod
    def copy_from(grade_moments):
        return StudentGradeMoments(grade_moments.name, grade_moments.assignment_group_ids)
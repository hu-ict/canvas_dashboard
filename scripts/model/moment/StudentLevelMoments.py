from scripts.model.moment.StudentMomentsBase import StudentMomentsBase


class StudentLevelMoments(StudentMomentsBase):
    @staticmethod
    def copy_from(level_moments):
        return StudentLevelMoments(level_moments.name, level_moments.assignment_group_ids)

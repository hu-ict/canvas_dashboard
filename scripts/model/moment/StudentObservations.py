from scripts.model.moment.StudentMomentsBase import StudentMomentsBase

class StudentObservations(StudentMomentsBase):
    @staticmethod
    def copy_from(observations):
        return StudentObservations(observations.name, observations.assignment_group_ids)
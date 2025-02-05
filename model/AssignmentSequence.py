from model.Assignment import Assignment
from model.LearningOutcome import LearningOutcome
from model.perspective.Status import MISSED_ITEM


class AssignmentSequence:
    def __init__(self, name, tag, grading_type, points):
        self.name = name
        self.tag = tag
        self.grading_type = grading_type
        self.points = points
        self.assignments = []
        self.learning_outcomes = []

    def __str__(self):
        return f'AssignmentSequence({self.name}, {self.tag}, {self.grading_type}, {self.points})'

    def get_day(self):
        return self.assignments[0].assignment_day

    def get_date(self):
        return self.assignments[0].assignment_date

    def get_date_day(self, submission_sequence, actual_day):
        if len(self.assignments) > 0:
            index = 0
            for assignment in self.assignments:
                if submission_sequence is None:
                    if actual_day < assignment.assignment_day:
                        # deadline nog niet verstreken
                        return self.assignments[index].assignment_date, self.assignments[index].assignment_day
                    else:
                        # deadline verstreken
                        index += 1
                else:
                    submission = submission_sequence.get_submission_by_assignment_id(assignment.id)
                    if submission is None:
                        # niets ingeleverd
                        if actual_day < assignment.assignment_day:
                            # deadline nog niet verstreken
                            return self.assignments[index].assignment_date, self.assignments[index].assignment_day
                        else:
                            # deadline verstreken
                            index += 1
                    else:
                        # wel ingeleverd
                        if submission.graded:
                            # beoordeeld
                            if submission.score == submission.points:
                                # voldaan
                                return self.assignments[index].assignment_date, self.assignments[index].assignment_day
                            else:
                                # niet voldaan
                                index += 1
                        elif submission.status == MISSED_ITEM:
                            # niets ingeleverd
                            index += 1
                        else:
                            # nog niet beoordeeld
                            return self.assignments[index].assignment_date, self.assignments[index].assignment_day
            if index >= len(self.assignments):
                index = len(self.assignments) - 1
                return self.assignments[index].assignment_date, self.assignments[index].assignment_day
        return 0, 0

    def get_passed_assignments(self, actual_day):
        passed_assignments = []
        for assignment in self.assignments:
            if assignment.assignment_day < actual_day:
                passed_assignments.append(assignment)
        return passed_assignments

    def get_missed_assignments(self, instance, course, submission_sequence, actual_day):
        missed_assignments = []
        last_in_completed = False
        for assignment in self.assignments:
            if assignment.assignment_day < actual_day:
                if instance.is_instance_of("inno_courses") and (assignment.assignment_day > (course.days_in_semester - course.improvement_period)):
                    #missed alleen in de reguliere tijd
                    continue
                # deadline is verstreken
                if submission_sequence is None:
                    missed_assignments.append(assignment)
                else:
                    submission = submission_sequence.get_submission_by_assignment_id(assignment.id)
                    if submission is None:
                        missed_assignments.append(assignment)
                    else:
                        if submission.graded:
                            if submission.score == submission.points:
                                # voldaan
                                return missed_assignments
                            else:
                                # niet voldaan
                                pass
                        else:
                            # nog niet beoordeeld
                            return missed_assignments
        return missed_assignments

    def get_last_passed_assignment(self, actual_day):
        last_passed_assignment = None
        for assignment in self.assignments:
            if assignment.assignment_day < actual_day:
                last_passed_assignment = assignment
        return last_passed_assignment

    def add_learning_outcome(self, learning_outcome_id):
        if learning_outcome_id not in self.learning_outcomes:
            self.learning_outcomes.append(learning_outcome_id)

    def to_json(self):
        return {
            'name': self.name,
            'tag': self.tag,
            'grading_type': self.grading_type,
            'points': int(self.points),
            'assignments': list(map(lambda a: a.to_json(), self.assignments)),
            'learning_outcomes': self.learning_outcomes
        }

    @staticmethod
    def from_dict(data_dict):
        new = AssignmentSequence(data_dict['name'], data_dict['tag'], data_dict['grading_type'], data_dict['points'])
        if 'assignments' in data_dict.keys():
            new.assignments = list(map(lambda a: Assignment.from_dict(a), data_dict['assignments']))
        if 'learning_outcomes' in data_dict:
            new.learning_outcomes = data_dict['learning_outcomes']
        return new

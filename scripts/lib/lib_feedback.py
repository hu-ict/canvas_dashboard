from scripts.lib.lib_date import date_to_day
from scripts.lib.lib_text import get_extracted_text
from scripts.model.learning_outcome.Feedback import Feedback


def categorize_feedback(feedback_comment):
    feedback_list = []
    if '@' in feedback_comment:
        feedback_list = get_extracted_text(feedback_comment)
    else:
        feedback_list.append({"lu": "AF", "text": feedback_comment})
    return feedback_list


def get_feedback_from_submission(course, student, submission):
    # print("LSU81 -", submission.assignment.name)
    # algemeen commentaar veld
    for comment in submission.comments:
        # algemene comments in een Canvas submission
        feedback_date = comment.date
        feedback_day = date_to_day(course.start_date, feedback_date)
        feedback_list = categorize_feedback(comment.comment)
        # print("LSU80 - Student", student.email, "Submission", submission.assignment.name)
        # print("LSU80 -", len(feedback_list), comment.comment)
        for feedback_dict in feedback_list:
            # print("LSU81 -", feedback_dict)
            feedback = Feedback(comment.author_id, comment.author_name, feedback_date, feedback_day,
                                feedback_dict["text"], "N",
                                submission.assignment.name, submission.assignment.id, submission.grade, submission.grade)
            if 'LU' in feedback_dict["lu"].upper():
                if feedback_dict["lu"].upper() in student.learning_outcomes:
                    if feedback.comment[0] in "-+":
                        feedback.positive_neutral_negative = feedback.comment[0]
                    else:
                        feedback.positive_neutral_negative = "N"
                    student.learning_outcomes[feedback_dict["lu"].upper()].feedback_list.append(feedback)
                else:
                    print("LSU82 - Leeruitkomst uit comment niet gevonden in lijst van leeruitkomsten",
                          feedback_dict["lu"].upper(),
                          student.name,
                          submission.assignment.name,
                          comment.author_name,
                          comment.comment
                          )
                    feedback.comment = "Incorrecte @LUx tag. " + feedback.comment
                    student.general_feedback_list.append(feedback)
            else:
                student.general_feedback_list.append(feedback)
    # commentaar bij criterium
    if len(submission.rubrics) > 0:
        for criterion_score in submission.rubrics:
            feedback_date = submission.graded_date
            feedback_day = date_to_day(course.start_date, feedback_date)

            # print("BP10 -", submission.assignment.id, criterion_score)
            assignment = course.find_assignment(submission.assignment.id)
            # print("BP11 -", assignment)
            assignment_criterion = assignment.get_criterion(criterion_score.id)
            if assignment_criterion is None:
                continue
            # print("LSU84 -", len(assignment_criterion.learning_outcomes))
            if criterion_score.comment:
                # comments in rubrics
                # print("BP11 -", assignment_criterion, criterion_score)
                if criterion_score.rating_id and assignment_criterion.get_rating(criterion_score.rating_id) is not None:
                    rating_description = assignment_criterion.get_rating(criterion_score.rating_id).description
                    criterion_score_score = criterion_score.score
                elif submission.grade:
                    rating_description = submission.grade
                    criterion_score_score = submission.grade
                else:
                    rating_description = ""
                    criterion_score_score = "0"
                    # print("LSU88 -", assignment_criterion.learning_outcomes, criterion_score.comment)
                if len(assignment_criterion.learning_outcomes) == 1:
                    # de assignment rubric is gekoppeld aan een leeruitkomst
                    feedback = Feedback("id", submission.grader_name, feedback_date, feedback_day,
                                        criterion_score.comment, "N",
                                        submission.assignment.name + " (" + assignment_criterion.description + ")",
                                        submission.assignment.id, criterion_score_score, rating_description)
                    lu = assignment_criterion.learning_outcomes[0]
                    # print("LSU89 -", assignment_criterion.learning_outcomes, len(student.learning_outcomes[lu].feedback_list), student.learning_outcomes[lu])
                    student.learning_outcomes[lu].feedback_list.append(feedback)
                    # print("LSU91 -", assignment_criterion.learning_outcomes, len(student.learning_outcomes[lu].feedback_list), student.learning_outcomes[lu])
                else:
                    feedback_list = categorize_feedback(criterion_score.comment)
                    for feedback_dict in feedback_list:
                        feedback = Feedback("id", submission.grader_name, feedback_date, feedback_day,
                                            feedback_dict["text"], "N",
                                            submission.assignment.name + " (" + assignment_criterion.description + ")",
                                            submission.assignment.id, criterion_score_score, rating_description)
                        if 'LU' in feedback_dict["lu"].upper():
                            if feedback_dict["lu"].upper() in student.learning_outcomes:
                                if feedback.comment[0] in "-+":
                                    feedback.positive_neutral_negative = feedback.comment[0]
                                student.learning_outcomes[feedback_dict["lu"].upper()].feedback_list.append(feedback)
                            else:
                                feedback.comment = "Incorrecte @LUx annotatie. " + feedback.comment
                                student.general_feedback_list.append(feedback)
                                print("LSU91 - Leeruitkomst", feedback_dict["lu"].upper(), "niet gevonden", student.name,
                                      submission.assignment.name, submission.grader_name, criterion_score.comment)
                        else:
                            student.general_feedback_list.append(feedback)

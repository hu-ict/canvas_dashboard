from lib.lib_date import get_date_time_obj, date_to_day, get_actual_date, get_date_time_str
from model.Comment import Comment
from model.CriteriumScore import CriteriumScore
from model.Submission import Submission
from model.perspective.Status import MISSED_ITEM, NOT_CORRECT_GRADED, NOT_YET_GRADED, GRADED

NO_SUBMISSION = "Niets ingeleverd voor de deadline"
NO_SUBMISSION_GRADE = "Moet nog beoordeeld worden"
NO_DATA = "Geen data"
ROBOT = "Automatisch door systeem"


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def get_submission_date(a_course, a_canvas_submission, a_assignment):
    # bepaal de date/time van het datapunt
    if a_canvas_submission.submitted_at:
        submitted_date = get_date_time_obj(a_canvas_submission.submitted_at)
    else:
        submitted_date = a_assignment.assignment_date
    submitted_day = date_to_day(a_course.start_date, submitted_date)
    return submitted_date, submitted_day


def get_sum_score(a_submissions, a_start_date):
    l_sum_score = 0
    l_last_score = 0
    for submission in a_submissions:
        if submission.graded:
            l_sum_score += submission.score
            if l_last_score < date_to_day(a_start_date, submission.submitted_date):
                l_last_score = date_to_day(a_start_date, submission.submitted_date)
    return l_sum_score, l_last_score


def count_graded(results):
    l_graded = 0
    l_not_graded = 0
    for student in results.students:
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    if submission.submitted_day is not None and submission.submitted_day > 0:
                        if submission.graded:
                            l_graded += 1
                        else:
                            l_not_graded += 1
    return l_graded + l_not_graded, l_not_graded


def get_sum_score_print(a_submissions, a_start_date):
    l_sum_score = 0
    l_last_score = 0
    for submission in a_submissions:
        if submission.graded:
            l_sum_score += submission.score
            # print(submission.assignment_name, submission.score, l_sum_score)
            if l_last_score < date_to_day(a_start_date, submission.submitted_date):
                l_last_score = date_to_day(a_start_date, submission.submitted_date)
    return l_sum_score, l_last_score


def get_submitted_at(item):
    return item[1].submitted_at


def remove_assignment(a_assignments, a_submission):
    for i in range(0, len(a_assignments)):
        if a_assignments[i].id == a_submission.assignment_id:
            del a_assignments[i]
            return a_assignments
    return a_assignments


def get_rubric_score(rubrics_submission, student):
    total_rubric_score = 0.00
    criterium_scores = []
    error = False
    if rubrics_submission is not None:
        for canvas_criterium in rubrics_submission:
            # print("LS40 -", canvas_criterium)
            id = canvas_criterium[0]
            points = 0
            if 'points' in canvas_criterium[1].keys():
                points = canvas_criterium[1]['points']
                total_rubric_score += points
            else:
                error = True
                # f"FOUT De rubric bij de opdracht (Canvas-opdracht) is niet volledig gevuld. Opdracht is nu niet zichtbaar in portfolio of voortgang. Actie vereist!"
                # error = f"ERROR in criterium_score, student {student.name} group {student.group_id}, canvas_submission {canvas_criterium}, teacher action required."
            rating_id = canvas_criterium[1]['rating_id']
            comments = canvas_criterium[1]['comments']
            criterium_score = CriteriumScore(id, rating_id, points, comments)
            # print("LS42 -", criterium_score)
            criterium_scores.append(criterium_score)
    return criterium_scores, round(total_rubric_score, 2), error


def submission_builder(a_instance, a_course, a_student, a_assignment, a_canvas_submission, a_level_serie_collection):
    if a_canvas_submission.grade:
        graded = True
    else:
        if a_canvas_submission.grader_id:
            graded = True
        else:
            graded = False
    canvas_comments = a_canvas_submission.submission_comments
    if a_assignment.grading_type not in ["pass_fail", "points", "letter_grade"]:
        print("SB01 - unknown grading_type", a_assignment.grading_type)
        return
    if not a_canvas_submission.submitted_at and len(canvas_comments) == 0 and not graded:
        # print("SB02 - not graded AND no submission AND no comments for", a_assignment.name, a_student.name)
        return
    # print("SB05 -", graded, a_canvas_submission.grader_id)
    if not graded:
        grade_level = None
        grader_name = None
        grader_date = None
        l_submission = Submission(a_canvas_submission.id, a_assignment.group_id, a_assignment.id, a_student.id,
                                  a_assignment.name,
                                  a_assignment.assignment_date,
                                  a_assignment.assignment_day,
                                  None,
                                  None,
                                  NOT_YET_GRADED, graded, grade_level,
                                  grader_name, grader_date, 0,
                                  0, a_assignment.points, 0)
        for canvas_comment in canvas_comments:
            l_submission.comments.append(
                Comment(canvas_comment['author_id'],
                        canvas_comment['author_name'],
                        get_date_time_obj(canvas_comment['created_at']),
                        canvas_comment['comment']))
        l_submission.submitted_date, l_submission.submitted_day = get_submission_date(a_course, a_canvas_submission, a_assignment)
        return l_submission

    errors = []
    rubrics_scores = []
    rubric_score = 0
    if len(a_assignment.rubrics) > 0:
        has_assignment_rubric = True
        if hasattr(a_canvas_submission, "rubric_assessment") and len(a_canvas_submission.rubric_assessment.items()) > 0:
            canvas_submission_rubrics = a_canvas_submission.rubric_assessment.items()
            rubrics_scores, rubric_score, error = get_rubric_score(canvas_submission_rubrics, a_student)
            if error:
                has_submission_rubrics = False
            else:
                has_submission_rubrics = True
        else:
            has_submission_rubrics = False
    else:
        has_submission_rubrics = False
        has_assignment_rubric = False
    # maak een submission en voeg de commentaren toe
    # print("LS31 -", f"submission_builder [{graded}] [{a_canvas_submission.submitted_at}] grade {a_canvas_submission.grade} grader_id {a_canvas_submission.grader_id} comments {len(canvas_comments)} score {a_canvas_submission.score} grading_type {a_assignment.grading_type} and student {a_student.name}.")

    submission_score = 0.0
    grade_value = None
    if has_assignment_rubric and has_submission_rubrics and a_assignment.grading_type == "pass_fail":
        if a_canvas_submission.grade == 'complete':
            if a_canvas_submission.score is not None:
                # INNO en PROP-peil vd/nvd met rubrics voor de "echte" punten (verborgen voor studenten)
                if a_canvas_submission.score == 0:
                    submission_score = round(rubric_score, 1)
                else:
                    submission_score = round(a_canvas_submission.score, 1)
            else:
                submission_score = round(rubric_score, 1)
            grade_value = submission_score
        elif a_canvas_submission.grade == 'incomplete':
            l_perspective = a_course.find_perspective_by_assignment_group(a_assignment.group_id)
            submission_score = rubric_score
            if l_perspective in a_course.perspectives:
                l_level_series = a_level_serie_collection.level_series[a_course.perspectives[l_perspective.name].levels]
                # gebruik canvas_submission_rubrics
                grade = l_level_series.get_grade_by_fraction(submission_score / a_assignment.points)
                if grade is None:
                    print("LS45 -", l_level_series.name, submission_score, a_assignment.points)
                grade_value = round(grade.value*a_assignment.points, 1)
            else:
                # level_moments or grade_moments
                grade_value = submission_score

    if not has_assignment_rubric and a_assignment.grading_type == "pass_fail":
        if a_canvas_submission.grade == 'complete':
            submission_score = round(a_assignment.points, 1)
        elif a_canvas_submission.grade == 'incomplete':
            # geen waarde wanneer incomplete
            submission_score = round(0, 1)
        grade_value = submission_score

    if has_assignment_rubric and not has_submission_rubrics and a_assignment.grading_type == "pass_fail":
        if a_assignment.group_id == a_course.level_moments.assignment_groups[0]:
            # als er rubrics achter een peilmoment zit moet deze gebuikt worden, zo niet fout
            errors.append(
                f"FOUT Er is een rubric gedefinieerd bij het peilmonent (Canvas-opdracht), maar deze wordt niet gebruikt of is niet compleet ingevuld. Opdracht is nu niet zichtbaar in portfolio of voortgang. Actie vereist!")
            print("SB51 -", errors[-1])
        elif a_canvas_submission.grade == 'complete':
            if a_instance.is_instance_of('inno_courses'):
                errors.append(
                    f"FOUT Er is een rubric gedefinieerd bij de opdracht (Canvas-opdracht resultaat COMPLETE), maar deze wordt niet gebruikt of is niet compleet ingevuld. Opdracht is nu niet zichtbaar in portfolio of voortgang. Actie vereist!")
                print("SB52 -", errors[-1])
            else:
                # PROP als rubrics niet ingevuld dan toch goed keuren bij "complete"
                submission_score = a_assignment.points
                grade_value = submission_score
        elif a_canvas_submission.grade == 'incomplete':
            errors.append(
                f"FOUT Er is een rubric gedefinieerd bij de opdracht (Canvas-opdracht resultaat INCOMPLETE), maar deze wordt niet gebruikt of is niet compleet ingevuld. Opdracht is nu niet zichtbaar in portfolio of voortgang. Actie vereist!")
            print("SB53 -", errors[-1])

    if not has_assignment_rubric and a_assignment.grading_type == "points":
        if a_canvas_submission.score is None:
            errors.append(
                f"FOUT Score is leeg {a_canvas_submission.grade} {a_canvas_submission.grader_id} voor opdracht {a_assignment.name} en student {a_student.name} groep_id {a_student.group_id}.")
            print("SB55 -", errors[-1])
        else:
            submission_score = round(a_canvas_submission.score, 2)
            grade_value = submission_score

    if has_assignment_rubric and not has_submission_rubrics and a_assignment.grading_type == "points":
        errors.append(
            f"FOUT Er is een rubric gedefinieerd bij de opdracht, maar deze wordt niet gebruikt of is niet compleet ingevuld. Opdracht is nu niet zichtbaar in portfolio of voortgang. Actie vereist!")
        print("SB53 -", errors[-1])

    if has_assignment_rubric and has_submission_rubrics and a_assignment.grading_type == "points":
        submission_score = round(rubric_score, 2)
        grade_value = submission_score

    if not has_assignment_rubric and a_assignment.grading_type == "letter_grade":
        submission_score = round(a_canvas_submission.score, 2)
        grade_value = submission_score

    if has_assignment_rubric and has_submission_rubrics and a_assignment.grading_type == "letter_grade":
        submission_score = round(rubric_score.score, 1)
        grade_value = submission_score

    if has_submission_rubrics and a_canvas_submission.score != round(rubric_score, 1):
        if a_assignment.id == 295123:
            # uitzondering voor opdracht CSC - MITRE ATTACK
            grade_value = submission_score

    grader_date = None
    if len(errors) > 0:
        graded = False
        status = NOT_CORRECT_GRADED
    else:
        status = GRADED
    if a_canvas_submission.grader_id is not None and a_canvas_submission.grader_id > 0:
        teacher = a_course.find_teacher(a_canvas_submission.grader_id)
        if teacher:
            grader_name = teacher.name
        else:
            grader_name = a_canvas_submission.grader_id
        if a_canvas_submission.graded_at:
            grader_date = get_date_time_obj(a_canvas_submission.graded_at)
    else:
        grader_name = "onbekend"

    grade_level = None
    if graded:
        perspective = a_course.find_perspective_by_assignment_group(a_assignment.group_id)
        # print("LS44 - Graded", graded, perspective.name)
        if perspective.name == "level_moments":
            grade_level = str(int(submission_score))
        if perspective.name == "grade_moments":
            grade_level = str(int(submission_score))
        elif perspective.name in a_course.perspectives:
            grade_obj = a_level_serie_collection.level_series[perspective.levels].get_grade_by_fraction(submission_score / a_assignment.points)
            grade_level = grade_obj.level
        else:
            pass
            # print("LS45 - Grade", grade)
    l_submission = Submission(a_canvas_submission.id, a_assignment.group_id, a_assignment.id, a_student.id,
                              a_assignment.name,
                              a_assignment.assignment_date,
                              a_assignment.assignment_day,
                              None,
                              None,
                              status, graded, grade_level, grader_name, grader_date, submission_score,
                              grade_value, a_assignment.points, 0)
    for canvas_comment in canvas_comments:
        # print("LS51 -", a_student.name, canvas_comment['comment'])
        l_submission.comments.append(Comment(canvas_comment['author_id'], canvas_comment['author_name'],
                                             get_date_time_obj(canvas_comment['created_at']),
                                             remove_html_tags(canvas_comment['comment'])))
    if rubrics_scores is not None:
        l_submission.rubrics = rubrics_scores
    if len(errors) > 0:
        # er is een fout opgetreden, waarschijnlijk in de rubrics
        for error in errors:
            l_submission.comments.append(
                Comment(0, "Systeem", get_date_time_obj(get_date_time_str(get_actual_date())), error))

    # bepaal de date/time van het datapunt
    l_submission.submitted_date, l_submission.submitted_day = get_submission_date(a_course, a_canvas_submission,
                                                                                  a_assignment)
    l_submission.messages = errors
    return l_submission


def add_missed_assignments(course, actual_day, student_perspective):
    if len(student_perspective.assignment_groups) == 1:
        assignment_group = course.find_assignment_group(student_perspective.assignment_groups[0])
        if assignment_group is None:
            print("ASA06 - Assignment_group for perspective not found in course",
                  student_perspective.assignment_groups[0])
            return

        for assignment_sequence in assignment_group.assignment_sequences:
            submission_sequence = student_perspective.get_submission_sequence_by_tag(assignment_sequence.tag)
            missed_assignments = assignment_sequence.get_missed_assignments(submission_sequence, actual_day)
            # print("ASA07 - Missed assignments", len(missed_assignments))
            for assignment in missed_assignments:
                l_submission = Submission(0, assignment.group_id, assignment.id, 0, assignment.name,
                                          assignment.assignment_date,
                                          assignment.assignment_day,
                                          None,
                                          None,
                                          MISSED_ITEM, False, None, 0, 0, 0, 0, assignment.points, 0)
                l_submission.comments.append(Comment(0, ROBOT, assignment.assignment_date, NO_SUBMISSION))
                student_perspective.put_submission(assignment_sequence, l_submission)
    elif len(student_perspective.assignment_groups) > 1:
        print("LS07 - Perspective has more then one assignment_groups attached", student_perspective.name,
              student_perspective.assignment_groups)
    else:
        print("LS08 - Perspective has no assignment_groups attached", student_perspective.name,
              student_perspective.assignment_groups)


def add_open_level_moments(course, actual_day, student_id, student_level_moments):
    if len(student_level_moments.assignment_groups) == 1:
        assignment_group = course.find_assignment_group(student_level_moments.assignment_groups[0])
        if assignment_group is None:
            print("AOL02 - Assignment_group for perspective not found in course",
                  student_level_moments.assignment_groups[0])
            return
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                print("AOL04 -", assignment.name)
                if assignment.unlock_day <= actual_day:
                    if (assignment.assignment_day - actual_day) <= 7:
                        if student_level_moments.get_submission_by_assignment(assignment.id) is None:
                            print("AOL08 -", assignment.name, assignment.unlock_day, actual_day, assignment.assignment_day+21)
                            l_submission = Submission(0, assignment.group_id, assignment.id, student_id, assignment.name,
                                                      assignment.assignment_date,
                                                      assignment.assignment_day,
                                                      None,
                                                      None,
                                                      NOT_YET_GRADED, False, None, 0, 0, 0, 0, assignment.points, 0)
                            l_submission.comments.append(Comment(0, ROBOT, assignment.assignment_date, NO_SUBMISSION_GRADE))
                            student_level_moments.submissions.append(l_submission)
    elif len(student_level_moments.assignment_groups) > 1:
        print("AOL98 - Perspective has more then one assignment_groups attached", student_level_moments.name,
              student_level_moments.assignment_groups)
    else:
        print("AOL99 - Perspective has no assignment_groups attached", student_level_moments.name,
              student_level_moments.assignment_groups)


def read_submissions(a_instance, a_canvas_course, a_course, a_results, a_total_refresh, level_serie_collection):
    for assignment_group in a_course.assignment_groups:
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                print("RS10 - Processing Assignment {0:6} - {1} - {2} {4} points, grading: [{3}]".format(assignment.id, assignment_group.name,
                                                                              assignment.name, assignment.grading_type, assignment.points))
                if not a_total_refresh and ((a_results.actual_date - assignment.assignment_date).days > 10):
                    # deadline langer dan twee weken geleden. Alle feedback is gegeven.
                    continue
                if assignment.unlock_date is not None:
                    if assignment.unlock_date > a_results.actual_date:
                        # volgende assignment
                        continue
                if (assignment.assignment_date - a_results.actual_date).days > 10:
                    # deadline ligt nog 10 dagen ná actual_date
                    continue
                canvas_assignment = a_canvas_course.get_assignment(assignment.id, include=['submissions'])
                # print("LS12 -", canvas_assignment)
                if canvas_assignment is None:
                    print("RS15 - Could not find assignment", canvas_assignment.id, "within group", assignment_group.id)
                    continue
                canvas_submissions = canvas_assignment.get_submissions(include=['submission_comments', 'rubric_assessment'])
                # print("LS13 -", canvas_submissions)
                for canvas_submission in canvas_submissions:
                    # print("LS14 - canvas_submission", canvas_submission.id, canvas_submission.user_id)
                    student = a_results.find_student(canvas_submission.user_id)
                    if student is None:
                        # print("RS20 Could not find student", canvas_submission.user_id)
                        continue
                    l_submission = submission_builder(a_instance, a_course, student, assignment, canvas_submission, level_serie_collection)
                    # voeg een submission toe aan een van de perspectieven
                    # print(f"R31 Submission for {student.name}")
                    if l_submission is None:
                        # print(f"RS25 - Error creating submission {assignment.name} for student {student.name}")
                        continue
                    l_perspective = a_course.find_perspective_by_assignment_group(l_submission.assignment_group_id)
                    if l_perspective is None:
                        print(f"RS30 - Warning, could not find perspective for assignment_group {assignment_group.name}")
                        continue
                    if l_perspective.name == "level_moments":
                        if "online_text_entry" in assignment.submission_types:
                            l_submission.body = canvas_submission.body
                        if a_total_refresh:
                            student.student_level_moments.submissions.append(l_submission)
                        else:
                            student.student_level_moments.put_submission(l_submission)
                        # print("LS18 - PERSPECTIVE level_moments")
                    else:
                        # print("LS19 -", student.perspectives.keys())
                        student_perspective = student.perspectives[l_perspective.name]
                        if student_perspective is not None:
                            student_perspective.put_submission(assignment_sequence, l_submission)

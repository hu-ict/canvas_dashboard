from model.perspective.Status import NOT_YET_GRADED


def create_total_progress(instance, course):
    peilen = {}
    grades = {}
    for peil in course.level_moments.moments:
        peilen[peil] = {
            'overall': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }
    for grade in course.grade_moments.moments:
        grades[grade] = {
            'overall': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }
    student_total_progress = {
        'level_moments': peilen,
        'grade_moments': grades,
        'actual_progress': {
            'overall': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
        }
    }
    for perspective in course.perspectives.keys():
        student_total_progress["actual_progress"][perspective] = {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    return student_total_progress


def student_total(a_perspective):
    cum_score = 0
    for submission_sequence in a_perspective.submission_sequences:
        cum_score += submission_sequence.get_score()
    return cum_score


def add_total(totals, total):
    totals.append(total)


def process_total_progress(a_instance, a_course, a_results, a_total_progress):
    for student_results in a_results.students:
        peil = student_results.progress
        # print(a_student.name, peil)
        a_total_progress['actual_progress']['overall'][peil] += 1
        for l_perspective in student_results.perspectives.values():
            a_total_progress['actual_progress'][l_perspective.name][int(l_perspective.progress)] += 1

        if a_course.level_moments is not None:
            for level_label in a_course.level_moments.moments:
                if a_instance.is_instance_of("inno_courses"):
                    submission = student_results.get_level_moment_submission_by_query([level_label, "student"])
                elif a_instance.is_instance_of("inno_courses_2026"):
                    submission = student_results.get_level_moment_submission_by_query([level_label, "student"])
                else:
                    submission = student_results.get_level_moment_submission_by_query([level_label])
                if submission is None or submission.status == NOT_YET_GRADED:
                    a_total_progress["level_moments"][level_label]['overall'][-1] += 1
                else:
                    a_total_progress["level_moments"][level_label]['overall'][int(submission.score)] += 1
        if a_course.grade_moments is not None:
            for grade_label in a_course.grade_moments.moments:
                if a_instance.is_instance_of("inno_courses"):
                    submission = student_results.get_grade_moment_submission_by_query([grade_label, "student"])
                elif a_instance.is_instance_of("inno_courses_2026"):
                    submission = student_results.get_grade_moment_submission_by_query([grade_label, "student"])
                else:
                    submission = student_results.get_grade_moment_submission_by_query([grade_label])
                if submission is None or submission.status == NOT_YET_GRADED:
                    a_total_progress["grade_moments"][grade_label]['overall'][-1] += 1
                else:
                    if submission.grade is not None:
                        a_total_progress["grade_moments"][grade_label]['overall'][int(submission.grade)] += 1

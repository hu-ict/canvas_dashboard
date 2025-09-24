from model.perspective.Status import NOT_YET_GRADED, NOT_CORRECT_GRADED
from model.workload.Workload import Workload
from model.workload.WorkloadTeacher import WorkloadTeacher


def get_teachers(course):
    teachers = set()
    for teacher in course.teachers:
        if teacher in teachers:
            pass
        else:
            if len(teacher.responsibilities) > 0:
                teachers.add(teacher)
    teacher_list = list(teachers)
    teacher_list = sorted(teacher_list, key=lambda t: t.initials)
    return teacher_list


def create_workload(teachers):
    workload = Workload(1)
    for teacher in teachers:
        workload.workload_teachers.append(WorkloadTeacher(teacher.id, teacher.initials, teacher.name, 0, 0, 0))
    teacher_list = sorted(workload.workload_teachers, key=lambda t: t.initials)
    workload.workload_teachers = teacher_list
    return workload


def student_total(a_perspective):
    cum_score = 0
    for submission_sequence in a_perspective.submission_sequences:
        cum_score += submission_sequence.get_score()
    return cum_score


def add_total(totals, total):
    totals.append(total)


def get_submitted_at(item):
    return item.submitted_at


def check_for_late(a_course, a_submission, a_workload, a_actual_day):
    if a_submission.status == NOT_YET_GRADED or a_submission.status == NOT_CORRECT_GRADED:
        student = a_course.find_student(a_submission.student_id)
        assessor = student.get_assessor_by_assignment_group(a_submission.assignment_group_id)
        if assessor is not None:
            # print("BTW82", student.name, assessor)
            workload_teacher = a_workload.get_workload_teacher(assessor.teacher_id)
            if a_submission.submitted_day is None:
                late_days = a_actual_day - a_submission.assignment_day
            else:
                late_days = a_actual_day - a_submission.submitted_day
            if late_days <= 7:
                workload_teacher.w1_count += 1
            elif 7 < late_days <= 14:
                workload_teacher.w2_count += 1
            else:
                workload_teacher.w3_count += 1
            workload_teacher.worklist.append(a_submission.to_json())
        else:
            print("BTW85 - No assessor for assignment_group_id", a_submission.assignment_group_id, student.name)


def get_workload(a_course, a_results, a_workload):
    for student_results in a_results.students:
        for perspective in student_results.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    check_for_late(a_course, submission, a_workload, a_results.actual_day)

        for submission in student_results.student_level_moments.submissions:
            # print("BT87 -", student_results.student_level_moments.name, submission)
            # print("BT89 -", list(a_student_totals['perspectives'][student_results.student_level_moments.name]['list']))
            check_for_late(a_course, submission, a_workload, a_results.actual_day)
        for submission in student_results.student_grade_moments.submissions:
            # print("BT87 -", student_results.student_grade_moments.name, submission)
            # print("BT88 -", submission.status)
            # print("BT89 -", list(a_student_totals['perspectives'][student_results.student_level_moments.name]['list']))
            check_for_late(a_course, submission, a_workload, a_results.actual_day)
    return a_workload



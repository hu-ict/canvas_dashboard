from lib.lib_date import date_to_day
from lib.lib_plotly import peil_labels


def student_total(a_perspective):
    cum_score = 0
    for l_submission in a_perspective:
        cum_score += l_submission.score
    return cum_score


def add_total(totals, total):
    totals.append(total)


def get_submitted_at(item):
    return item.submitted_at


def count_student(a_start, a_student_totals, a_student):
    peil = a_student.progress
    # print(a_student.name, peil)
    a_student_totals[a_start.progress.name]['Actueel']['overall'][peil] += 1
    for l_perspective in a_student.perspectives.values():
        add_total(a_student_totals['perspectives'][l_perspective.name]['count'], int(student_total(l_perspective.submissions)))
    for peil_label in peil_labels[1:]:
        peil = a_student.get_peilmoment_by_query([peil_label, "overall"])
        if peil:
            a_student_totals["progress"][peil_label]['overall'][peil.score] += 1
        else:
            a_student_totals["progress"][peil_label]['overall'][-1] += 1


def check_for_late(a_instances, a_course, a_student_totals, a_student, a_submission, a_perspective, a_actual_day):
    if not a_submission.graded:
        if a_student.coach != "None":
            if a_perspective == 'team':
                l_selector = a_course.find_teacher(a_student.coach).initials
            else:
                l_selector = a_student.role
        else:
            if a_instances.is_instance_of("inno_courses") or a_instances.is_instance_of("inno_courses_new"):
                l_selector = a_student.role
            else:
                l_selector = a_course.find_student_group(a_student.group_id).name
        late_days = a_actual_day - a_submission.submitted_day
        a_student_totals['perspectives'][a_perspective]['list'][l_selector].append(a_submission.to_json())
        if late_days <= 7:
            a_student_totals['perspectives'][a_perspective]['pending'][l_selector] += 1
        elif 7 < late_days <= 14:
            a_student_totals['perspectives'][a_perspective]['late'][l_selector] += 1
        else:
            a_student_totals['perspectives'][a_perspective]['to_late'][l_selector] += 1
        add_total(a_student_totals['late']['count'], late_days)


def build_totals(a_instances, a_start, a_course, a_results, a_student_totals):
    for l_student in a_results.students:
        count_student(a_start, a_student_totals, l_student)
        for l_perspective in l_student.perspectives.values():
            for l_submission in l_perspective.submissions:
                check_for_late(a_instances, a_course, a_student_totals, l_student, l_submission, l_perspective.name,
                               date_to_day(a_start.start_date,  a_results.actual_date))

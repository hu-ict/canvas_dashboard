def student_total(a_perspective):
    cum_score = 0
    for l_submission in a_perspective:
        cum_score += l_submission.score
    return cum_score


def get_peil(a_perspective, a_query):
    for l_submission in a_perspective:
        condition = 0
        for item in a_query:
            if item in l_submission.assignment_name:
                condition += 1
        if condition == len(a_query):
            return int(l_submission.score)
    return -1


def add_total(totals, total):
    totals.append(total)
    # if total not in totals.keys():
    #     totals[total] = 1
    # else:
    #     totals[total] += 1


def get_submitted_at(item):
    return item.submitted_at


def count_student(a_student_totals, a_student):
    for l_perspective in a_student.perspectives:
        if l_perspective.name == "peil":
            a_student_totals[l_perspective.name]["Peilmoment halfweg"][get_peil(l_perspective.submissions, ["halfweg", "Overall"])] += 1
        elif l_perspective.name == "kennis":
            add_total(a_student_totals[l_perspective.name]['count'], int(student_total(l_perspective.submissions)))
        else:
            add_total(a_student_totals[l_perspective.name]['count'], int(student_total(l_perspective.submissions)))


def check_for_late(a_student_totals, a_submissions_late, a_student, a_submission, a_perspective, a_actual_date):
    if not a_submission.graded:
        if a_student.coach_initials != "None":
            if a_perspective == 'team':
                l_selector = a_student.coach_initials
            else:
                l_selector = a_student.get_role()
        else:
            l_selector = a_student.get_role()
        late_days = (a_actual_date - a_submission.submitted_at).days
        if late_days <= 7:
            a_student_totals[a_perspective]['pending'][l_selector] += 1
        else:
            a_submissions_late[a_perspective][l_selector].append(a_submission.to_json())
            if 7 < late_days <= 14:
                a_student_totals[a_perspective]['late'][l_selector] += 1
            else:
                a_student_totals[a_perspective]['to_late'][l_selector] += 1
        add_total(a_student_totals['late']['count'], late_days)


def build_totals(a_results, a_student_totals, a_submissions_late):
    for student_group in a_results.student_groups:
        for student in student_group.students:
            count_student(a_student_totals, student)
            for perspective in student.perspectives:
                for submission in perspective.submissions:
                    check_for_late(a_student_totals, a_submissions_late, student, submission, perspective.name, a_results.actual_date)








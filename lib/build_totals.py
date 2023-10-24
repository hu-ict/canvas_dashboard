def student_total(a_perspective):
    cum_score = 0
    for l_submission in a_perspective:
        cum_score += l_submission.score
    return cum_score


def get_actual_progress(a_perspectives):
    l_sum = 0
    l_progress = 5
    for l_perspective in a_perspectives:
        if l_perspective.name == 'peil':
            pass
        else:
            if l_perspective.progress < l_progress:
                l_progress = l_perspective.progress
            l_sum += l_perspective.progress
    if l_progress == 0:
        if l_sum == 0:
            return 0
        else:
            return 1
    elif l_progress == 1:
        return 1
    elif l_progress == 5:
        return -1
    else:
        if l_sum > 7:
            return 3
        else:
            return 2


def get_progress(a_perspective, a_query):
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


def get_submitted_at(item):
    return item.submitted_at


def count_student(a_student_totals, a_student):
    peil = get_actual_progress(a_student.perspectives)
    # print(a_student.name, peil)
    a_student_totals['peil']["Actueel"]['overall'][peil] += 1
    for l_perspective in a_student.perspectives:
        if l_perspective.name == "peil":
            peil = get_progress(l_perspective.submissions, ["halfweg", "Overall"])
            a_student_totals[l_perspective.name]["Sprint 4"]['overall'][peil] += 1
            peil = get_progress(l_perspective.submissions, ["Sprint 7", "Overall"])
            a_student_totals[l_perspective.name]["Sprint 7"]['overall'][peil] += 1
            peil = get_progress(l_perspective.submissions, ["Beoordeling", "Overall"])
            a_student_totals[l_perspective.name]["Beoordeling"]['overall'][peil] += 1

            # peil = get_peil(l_perspective.submissions, ["halfweg", "Kennis"])
            # a_student_totals[l_perspective.name]["Sprint 4"]['kennis'][peil] += 1
            # peil = get_peil(l_perspective.submissions, ["Sprint 7", "Kennis"])
            # a_student_totals[l_perspective.name]["Sprint 7"]['kennis'][peil] += 1
            # peil = get_peil(l_perspective.submissions, ["Beoordeling", "Kennis"])
            # a_student_totals[l_perspective.name]["Beoordeling"]['kennis'][peil] += 1
            #
            # peil = get_peil(l_perspective.submissions, ["halfweg", "Gilde"])
            # a_student_totals[l_perspective.name]["Sprint 4"]['gilde'][peil] += 1
            # peil = get_peil(l_perspective.submissions, ["Sprint 7", "Gilde"])
            # a_student_totals[l_perspective.name]["Sprint 7"]['gilde'][peil] += 1
            # peil = get_peil(l_perspective.submissions, ["Beoordeling", "Gilde"])
            # a_student_totals[l_perspective.name]["Beoordeling"]['gilde'][peil] += 1
            #
            # peil = get_peil(l_perspective.submissions, ["halfweg", "Team"])
            # a_student_totals[l_perspective.name]["Sprint 4"]['team'][peil] += 1
            # peil = get_peil(l_perspective.submissions, ["Sprint 7", "Team"])
            # a_student_totals[l_perspective.name]["Sprint 7"]['team'][peil] += 1
            # peil = get_peil(l_perspective.submissions, ["Beoordeling", "Team"])
            # a_student_totals[l_perspective.name]["Beoordeling"]['team'][peil] += 1
        else:
            add_total(a_student_totals['perspectives'][l_perspective.name]['count'], int(student_total(l_perspective.submissions)))


def check_for_late(a_student_totals, a_student, a_submission, a_perspective, a_actual_date):
    if not a_submission.graded:
        if a_student.coach_initials != "None":
            if a_perspective == 'team':
                l_selector = a_student.coach_initials
            else:
                l_selector = a_student.get_role()
        else:
            l_selector = a_student.get_role()
        late_days = (a_actual_date - a_submission.submitted_date).days

        a_student_totals['perspectives'][a_perspective]['list'][l_selector].append(a_submission.to_json())
        if late_days <= 7:
            a_student_totals['perspectives'][a_perspective]['pending'][l_selector] += 1
        else:
            if 7 < late_days <= 14:
                a_student_totals['perspectives'][a_perspective]['late'][l_selector] += 1
            else:
                a_student_totals['perspectives'][a_perspective]['to_late'][l_selector] += 1
        add_total(a_student_totals['late']['count'], late_days)


def build_totals(a_results, a_student_totals):
    for l_student in a_results.students:
        count_student(a_student_totals, l_student)
        for l_perspective in l_student.perspectives:
            for l_submission in l_perspective.submissions:
                check_for_late(a_student_totals, l_student, l_submission, l_perspective.name, a_results.actual_date)








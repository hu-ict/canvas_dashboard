from lib.file import tennant


def student_total(a_perspective):
    cum_score = 0
    for l_submission in a_perspective:
        cum_score += l_submission.score
    return cum_score


def get_actual_progress(a_perspectives):
    l_sum = 0
    # determine lowest progress
    l_progress = 5
    is_prop = False
    for l_perspective in a_perspectives.values():
        if l_perspective.name == 'final':
            is_prop = True
        if l_perspective.name == 'peil':
            pass
        else:
            if l_perspective.progress < l_progress:
                l_progress = l_perspective.progress
            l_sum += l_perspective.progress
    if l_progress == 0:
        if l_sum == 0:
            # no progress at all
            return 0
        else:
            # minimal one perspective with some progress
            return 1
    elif l_progress == 1:
        # lowest progress 1
        return 1
    elif l_progress == 5:
        # progress unknown
        return -1
    else:
        if is_prop:
            if l_sum > 6:
                return 3
            else:
                return 2
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


def count_student(a_course, a_student_totals, a_student):
    peil = get_actual_progress(a_student.perspectives)
    # print(a_student.name, peil)
    a_student_totals['peil']['Actueel']['overall'][peil] += 1
    for l_perspective in a_student.perspectives.values():
        if l_perspective.name == a_course.progress_perspective:
            peil = get_progress(l_perspective.submissions, ["Sprint 4", "Overall"])
            a_student_totals[l_perspective.name]["Sprint 4"]['overall'][peil] += 1
            peil = get_progress(l_perspective.submissions, ["Sprint 7", "Overall"])
            a_student_totals[l_perspective.name]["Sprint 7"]['overall'][peil] += 1
            peil = get_progress(l_perspective.submissions, ["Beoordeling", "Overall"])
            a_student_totals[l_perspective.name]["Beoordeling"]['overall'][peil] += 1
        else:
            add_total(a_student_totals['perspectives'][l_perspective.name]['count'], int(student_total(l_perspective.submissions)))


def check_for_late(a_course, a_student_totals, a_student, a_submission, a_perspective, a_actual_date):
    if not a_submission.graded:
        if a_student.coach != "None":
            if a_perspective == 'team':
                l_selector = a_course.find_teacher(a_student.coach).initials
            else:
                l_selector = a_student.role
        else:
            if tennant == "inno":
                l_selector = a_student.role
            else:
                l_selector = a_course.find_student_group(a_student.group_id).name
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


def build_totals(a_course, a_results, a_student_totals, a_gilde, a_coaches):
    for l_student in a_results.students:
        count_student(a_course, a_student_totals, l_student)
        for l_perspective in l_student.perspectives.values():
            if l_perspective.name == "gilde":
                for l_submission in l_perspective.submissions:
                    if int(l_submission.score) in a_gilde[l_student.role]:
                        a_gilde[l_student.role][int(l_submission.score)] += 1
                    else:
                        a_gilde[l_student.role][int(l_submission.score)] = 1
            if l_perspective.name == "team":
                for l_submission in l_perspective.submissions:
                    # print(type(l_student.coach), l_student.coach, a_coaches[l_student.coach])
                    if int(l_submission.score) in a_coaches[l_student.coach]:
                        a_coaches[l_student.coach][int(l_submission.score)] += 1
                    else:
                        a_coaches[l_student.coach][int(l_submission.score)] = 1
            if l_perspective.name == "peil":
                continue
            for l_submission in l_perspective.submissions:
                check_for_late(a_course, a_student_totals, l_student, l_submission, l_perspective.name, a_results.actual_date)

    for l_gilde in a_gilde:
        l_total = 0
        for point in a_gilde[l_gilde].values():
            l_total += point
        for point in a_gilde[l_gilde]:
            a_gilde[l_gilde][point] = int(a_gilde[l_gilde][point]*100/l_total*10)/10
        a_gilde[l_gilde] = dict(sorted(a_gilde[l_gilde].items()))

    # for l_coach in a_coaches:
    #     l_total = 0
    #     for point in a_coaches[l_coach]:
    #         l_total += point
    #     for point in a_coaches[l_coach]:
    #         a_coaches[l_coach.id][point] = int(a_coaches[l_coach][point]*100/l_total*10)/10
    #     a_coaches[l_coach] = dict(sorted(a_coaches[l_coach].items()))










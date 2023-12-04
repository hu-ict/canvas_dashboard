def student_total(a_perspective):
    cum_score = 0
    for l_submission in a_perspective:
        cum_score += l_submission.score
    return cum_score


def get_actual_progress(a_perspectives):
    boven = 7
    for l_perspective in a_perspectives.values():
        if l_perspective.name == 'team':
            boven = 8
    l_progress = []
    for l_perspective in a_perspectives.values():
        if l_perspective.name != "peil" and l_perspective.name != "aanwezig":
            l_progress.append(l_perspective.progress)
    if len(l_progress) == 3:
        if l_progress[0] >= 2 and l_progress[1] >= 2 and l_progress[2] >= 2:
            if sum(l_progress) >= boven:
                # boven niveau
                return 3
            else:
                # op niveau
                return 2
        elif l_progress[0] <= 1 or l_progress[1] <= 1 or l_progress[2] <= 1:
            # minimaal onder niveau
            if l_progress[0] == -1 and l_progress[1] == -1 and l_progress[2] == -1:
                # niet te bepalen
                return -1
            elif l_progress[0] <= 0 and l_progress[1] <= 0 and l_progress[2] <= 0:
                # geen activiteit in semester ná deadlines
                return 0
            else:
                return 1
        else:
            return -2
    return -1

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


def count_student(a_start, a_course, a_student_totals, a_student):
    peil = get_actual_progress(a_student.perspectives)
    # print(a_student.name, peil)
    a_student_totals['peil']['Actueel']['overall'][peil] += 1
    for l_perspective in a_student.perspectives.values():
        if l_perspective.name == a_start.progress_perspective:
            peil = get_progress(l_perspective.submissions, ["Sprint 4", "Overall"])
            a_student_totals[l_perspective.name]["Sprint 4"]['overall'][peil] += 1
            peil = get_progress(l_perspective.submissions, ["Sprint 7", "Overall"])
            a_student_totals[l_perspective.name]["Sprint 7"]['overall'][peil] += 1
            peil = get_progress(l_perspective.submissions, ["Beoordeling", "Overall"])
            a_student_totals[l_perspective.name]["Beoordeling"]['overall'][peil] += 1
        else:
            add_total(a_student_totals['perspectives'][l_perspective.name]['count'], int(student_total(l_perspective.submissions)))


def check_for_late(a_instances, a_course, a_student_totals, a_student, a_submission, a_perspective, a_actual_date):
    if not a_submission.graded:
        if a_student.coach != "None":
            if a_perspective == 'team':
                l_selector = a_course.find_teacher(a_student.coach).initials
            else:
                l_selector = a_student.role
        else:
            if a_instances.is_instance_of("inno_courses"):
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


def build_totals(a_instances, a_start, a_course, a_results, a_student_totals):
    for l_student in a_results.students:
        count_student(a_start, a_course, a_student_totals, l_student)
        for l_perspective in l_student.perspectives.values():
            if l_perspective.name == "peil":
                continue
            for l_submission in l_perspective.submissions:
                check_for_late(a_instances, a_course, a_student_totals, l_student, l_submission, l_perspective.name, a_results.actual_date)










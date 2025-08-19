from model.perspective.Status import NOT_YET_GRADED, NOT_CORRECT_GRADED


def init_sections_count(course):
    count = {}
    for section in course.sections:
        count[section.name] = 0
    return count


def init_sections_list(course):
    l_list = {}
    for section in course.sections:
        l_list[section.name] = []
    return l_list


def init_sections_dict(course):
    l_list = {}
    for section in course.sections:
        l_list[section.name] = {}
    return l_list


def init_roles_count(course):
    role_count = {}
    for role in course.roles:
        role_count[role.short] = 0
    return role_count


def init_roles_list(course):
    l_list = {}
    for role in course.roles:
        l_list[role.short] = []
    return l_list


def init_roles_dict(course):
    l_list = {}
    for role in course.roles:
        l_list[role.short] = {}
    return l_list


def init_teacher_count(teachers):
    count = {}
    for teacher in teachers.values():
        count[teacher["teacher"].initials] = 0
    return count


def init_teacher_list(coaches):
    team_list = {}
    for coach in coaches.values():
        team_list[coach["teacher"].initials] = []
    return team_list


def init_teachers_dict(a_course, groups):
    def get_initials(item):
        return item[1]['teacher'].initials

    l_teachers = {}
    # for teacher in a_course.teachers:
    #     if len(teacher.projects) > 0:
    #         l_coaches[teacher.initials] = {}

    for group in groups:
        if len(group.teachers) > 0:
            for teacher_id in group.teachers:
                teacher = a_course.find_teacher(teacher_id)
                l_teachers[teacher.id] = {'count': {}, 'teacher': teacher}
    l_teachers = dict(sorted(l_teachers.items(), key=lambda item: get_initials(item)))
    # print("GD81 -", l_coaches)
    return l_teachers


def create_total_workload(instance, course, project_teachers, guild_teachers):
    # for team_coach in team_coaches.values():
    # print("GD04 -", team_coach["teacher"])
    peilen = {}
    grades = {}
    if instance.is_instance_of("inno_courses"):
        for peil in course.level_moments.moments:
            peilen[peil] = {
                'overall': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
            }
        for grade in course.grade_moments.moments:
            grades[grade] = {
                'overall': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
            }
        student_totals = {
            'perspectives': {
                'team': {'count': [],
                         'pending': init_teacher_count(project_teachers),
                         'late': init_teacher_count(project_teachers),
                         'to_late': init_teacher_count(project_teachers),
                         'list': init_teacher_list(project_teachers)},
                'gilde': {'count': [],
                          'pending': init_teacher_count(guild_teachers),
                          'late': init_teacher_count(guild_teachers),
                          'to_late': init_teacher_count(guild_teachers),
                          'list': init_teacher_list(guild_teachers)},
                'kennis': {'count': [], 'pending': init_roles_count(course), 'late': init_roles_count(course),
                           'to_late': init_roles_count(course), 'list': init_roles_list(course)},
                'level_moments': {'count': [], 'pending': init_teacher_count(project_teachers),
                                  'late': init_teacher_count(project_teachers), 'to_late': init_teacher_count(project_teachers),
                                  'list': init_teacher_list(project_teachers)},
                'grade_moments': {'count': [], 'pending': init_teacher_count(project_teachers),
                                  'late': init_teacher_count(project_teachers), 'to_late': init_teacher_count(project_teachers),
                                  'list': init_teacher_list(project_teachers)},
            },
            'late': {'count': []}
        }
    elif instance.is_instance_of("courses_2026"):
        for peil in course.level_moments.moments:
            peilen[peil] = {
                'overall': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
            }
        for grade in course.grade_moments.moments:
            grades[grade] = {
                'overall': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
            }
        student_totals = {
            'perspectives': {
                'portfolio': {'count': [],
                         'pending': init_teacher_count(project_teachers),
                         'late': init_teacher_count(project_teachers),
                         'to_late': init_teacher_count(project_teachers),
                         'list': init_teacher_list(project_teachers)},
                'level_moments': {'count': [], 'pending': init_teacher_count(project_teachers),
                                  'late': init_teacher_count(project_teachers), 'to_late': init_teacher_count(project_teachers),
                                  'list': init_teacher_list(project_teachers)},
                'grade_moments': {'count': [], 'pending': init_teacher_count(project_teachers),
                                  'late': init_teacher_count(project_teachers), 'to_late': init_teacher_count(project_teachers),
                                  'list': init_teacher_list(project_teachers)},
            },
            'late': {'count': []}
        }

    elif instance.is_instance_of("prop_courses"):
        for peil in course.level_moments.moments:
            peilen[peil] = {
                'overall': range
            }
        for grade in course.grade_moments.moments:
            grades[grade] = {
                'overall': range
            }
        student_totals = {

            'perspectives': {},
            'level_moments': peilen,
            'grade_moments': grades,
            'late': {'count': []}
        }
        for perspective in course.perspectives.keys():
            student_totals["perspectives"][perspective] = {'count': [], 'pending': init_sections_count(course),
                                                           'late': init_sections_count(course),
                                                           'to_late': init_sections_count(course),
                                                           'list': init_sections_list(course)}

        student_totals["perspectives"]["level_moments"] = {'count': [], 'pending': init_sections_count(course),
                                                           'late': init_sections_count(course),
                                                           'to_late': init_sections_count(course),
                                                           'list': init_sections_list(course)}
        if course.level_moments is not None:
            student_totals["level_moments"] = {}
            for moment in course.level_moments.moments:
                student_totals["level_moments"][moment] = {'overall': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}}
                for perspective in course.perspectives.keys():
                    student_totals["level_moments"][moment][perspective] = {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}

        student_totals["perspectives"]["grade_moments"] = {'count': [], 'pending': init_sections_count(course),
                                                           'late': init_sections_count(course),
                                                           'to_late': init_sections_count(course),
                                                           'list': init_sections_list(course)}
        if course.grade_moments is not None:
            student_totals["grade_moments"] = {}
            for moment in course.grade_moments.moments:
                student_totals["grade_moments"][moment] = {'overall': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0}}
                for perspective in course.perspectives.keys():
                    student_totals["grade_moments"][moment][perspective] = {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}

        student_totals["actual_progress"] = {'overall': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}}
        for perspective in course.perspectives.keys():
            student_totals["actual_progress"][perspective] = {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
    else:
        student_totals = {
            'student_count': 0,
            'perspectives': {},
            'level_moments': {},
            'late': {'count': []}
        }
        for perspective in course.perspectives:
            student_totals['perspectives'][perspective] = {'count': [], 'pending': init_sections_count(course),
                                                           'late': init_sections_count(course),
                                                           'to_late': init_sections_count(course),
                                                           'list': init_sections_list(course)}
        if course.level_moments is not None:
            student_totals['perspectives'][course.level_moments.name] = {'count': [],
                                                                         'pending': init_sections_count(course),
                                                                         'late': init_sections_count(course),
                                                                         'to_late': init_sections_count(course),
                                                                         'list': init_sections_list(course)}
    return student_totals


def student_total(a_perspective):
    cum_score = 0
    for submission_sequence in a_perspective.submission_sequences:
        cum_score += submission_sequence.get_score()
    return cum_score


def add_total(totals, total):
    totals.append(total)


def get_submitted_at(item):
    return item.submitted_at


def check_for_late(a_instance, a_course, a_total_workload, a_student_results, a_submission, a_perspective,
                   a_actual_day):
    student = a_course.find_student(a_student_results.id)
    if a_submission.status == NOT_YET_GRADED or a_submission.status == NOT_CORRECT_GRADED:
        # print("BT81", a_student.name, a_perspective, a_submission.assignment_name)
        if len(student.project_teachers) > 0:
            # print("BT82", a_student.name, a_student.coach)
            if a_instance.is_instance_of("inno_courses") or a_instance.is_instance_of("courses_2026"):
                if a_perspective == 'team':
                    l_selector = a_course.find_teacher(student.project_teachers[0]).initials
                elif a_perspective == 'gilde' and len(student.guild_teachers) > 0:
                    l_selector = a_course.find_teacher(student.guild_teachers[0]).initials
                elif a_perspective == 'level_moments' or a_perspective == 'grade_moments':
                    l_selector = a_course.find_teacher(student.project_teachers[0]).initials
                else:
                    l_selector = a_student_results.role
                # print("BT61 -", a_perspective, l_selector)
            elif a_instance.is_instance_of("prop_courses"):
                group = a_course.find_project_group(student.project_id)
                l_selector = group.name
            else:
                l_selector = a_student_results.role
        else:
            if a_instance.is_instance_of("inno_courses") or a_instance.is_instance_of("courses_2026"):
                # er moet een coach gekoppeld zijn
                return
            else:
                print("BT83 Group id", student.project_id)
                group = a_course.find_project_group(student.project_id)
                l_selector = group.name
            print("BT62 -", a_perspective, l_selector)
        if a_submission.submitted_day is None:
            late_days = a_actual_day - a_submission.assignment_day
        else:
            late_days = a_actual_day - a_submission.submitted_day
        # if a_perspective == 'grade_moments':
        #     print("BT85 -", a_perspective, l_selector, a_submission.assignment_name)
        if l_selector in a_total_workload['perspectives'][a_perspective]['list']:
            a_total_workload['perspectives'][a_perspective]['list'][l_selector].append(a_submission.to_json())
            if late_days <= 7:
                a_total_workload['perspectives'][a_perspective]['pending'][l_selector] += 1
            elif 7 < late_days <= 14:
                a_total_workload['perspectives'][a_perspective]['late'][l_selector] += 1
            else:
                a_total_workload['perspectives'][a_perspective]['to_late'][l_selector] += 1
        # add_total(a_total_workload['late']['count'], late_days)


def process_total_workload(a_instance, a_course, a_results, a_student_totals):
    for student_results in a_results.students:
        for l_perspective in student_results.perspectives.values():
            for submission_sequence in l_perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    check_for_late(a_instance, a_course, a_student_totals, student_results, submission,
                                   l_perspective.name, a_results.actual_day)
        for submission in student_results.student_level_moments.submissions:
            # print("BT87 -", student_results.student_level_moments.name, submission)
            # print("BT89 -", list(a_student_totals['perspectives'][student_results.student_level_moments.name]['list']))
            check_for_late(a_instance, a_course, a_student_totals, student_results, submission,
                           student_results.student_level_moments.name, a_results.actual_day)
        for submission in student_results.student_grade_moments.submissions:
            # print("BT87 -", student_results.student_grade_moments.name, submission)
            # print("BT88 -", submission.status)
            # print("BT89 -", list(a_student_totals['perspectives'][student_results.student_level_moments.name]['list']))
            check_for_late(a_instance, a_course, a_student_totals, student_results, submission,
                           student_results.student_grade_moments.name, a_results.actual_day)


def build_late_email(a_course, a_total_workload):
    for perspective in a_total_workload['perspectives'].keys():
        selectors = a_total_workload['perspectives'][perspective]['late']
        for selector in selectors:
            late_count = a_total_workload['perspectives'][perspective]['late'][selector]
            to_late_count = a_total_workload['perspectives'][perspective]['to_late'][selector]
            if late_count > 0 or to_late_count > 0:
                print(f"Voor {selector} {perspective} zijn {late_count+to_late_count} items een week te laat, daarvan staan {to_late_count} items langer dan 2 weken open")



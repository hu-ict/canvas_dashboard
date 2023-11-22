import json
from lib.build_totals import build_totals
from lib.build_bootstrap import build_bootstrap_general
from lib.build_late import build_late
from lib.lib_plotly import peil_labels
from lib.plot_totals import plot_totals
from lib.file import read_course, read_start, read_results, read_progress, read_labels_colors, tennant


def init_sections_count():
    count = {}
    for section in course.sections:
        count[section.name] = 0
    return count


def init_sections_list():
    l_list = {}
    for section in course.sections:
        l_list[section.name] = []
    return l_list


def init_sections_dict():
    l_list = {}
    for section in course.sections:
        l_list[section.name] = {}
    return l_list


def init_roles_count():
    role_count = {}
    for role in course.roles:
        role_count[role.short] = 0
    return role_count


def init_roles_list():
    l_list = {}
    for role in course.roles:
        l_list[role.short] = []
    return l_list


def init_roles_dict():
    l_list = {}
    for role in course.roles:
        l_list[role.short] = {}
    return l_list


def init_coaches_count():
    team_count = {}
    for teacher in course.teachers:
        if len(teacher.projects) > 0:
            team_count[teacher.initials] = 0
    return team_count


def init_coaches_list():
    team_list = {}
    for teacher in course.teachers:
        if len(teacher.projects) > 0:
            team_list[teacher.initials] = []
    return team_list


def init_coaches_dict(a_course):
    def get_initials(item):
        return item[1]['teacher'].initials

    l_coaches = {}
    # for teacher in a_course.teachers:
    #     if len(teacher.projects) > 0:
    #         l_coaches[teacher.initials] = {}

    for group in a_course.student_groups:
        if len(group.teachers) > 0:
            for teacher_id in group.teachers:
                teacher = a_course.find_teacher(teacher_id)
                l_coaches[teacher.id] = {'count': {}, 'teacher': teacher}
    l_coaches = dict(sorted(l_coaches.items(), key=lambda item: get_initials(item)))
    return l_coaches


start = read_start()
course = read_course(start.course_file_name)
results = read_results(start.results_file_name)
labels_colors = read_labels_colors("labels_colors.json")
actual_day = (results.actual_date - course.start_date).days

peilen = {}
for peil in peil_labels:
    peilen[peil] = {
            'overall': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'team': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'gilde': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'kennis': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
        }
if tennant == "inno":
    student_totals = {
        'student_count': 0,
        'perspectives': {
            'team': {'count': [], 'pending': init_coaches_count(), 'late': init_coaches_count(), 'to_late': init_coaches_count(), 'list': init_coaches_list()},
            'gilde': {'count': [], 'pending': init_roles_count(), 'late': init_roles_count(), 'to_late': init_roles_count(), 'list': init_roles_list()},
            'kennis': {'count': [], 'pending': init_roles_count(), 'late': init_roles_count(), 'to_late': init_roles_count(), 'list': init_roles_list()}
        },
        'peil': peilen,
        'late': {'count': []}
    }
else:
    student_totals = {
        'student_count': 0,
        'perspectives': {
            'final': {'count': [], 'pending': init_sections_count(), 'late': init_sections_count(), 'to_late': init_sections_count(), 'list': init_sections_list()},
            'toets': {'count': [], 'pending': init_sections_count(), 'late': init_sections_count(), 'to_late': init_sections_count(), 'list': init_sections_list()},
            'project': {'count': [], 'pending': init_sections_count(), 'late': init_sections_count(), 'to_late': init_sections_count(), 'list': init_sections_list()}
        },
        'peil': peilen,
        'late': {'count': []}
    }

gilde = init_roles_dict()
team_coaches = init_coaches_dict(course)

print("build_bootstrap(course, results)")
build_bootstrap_general(course, results, team_coaches, labels_colors)

print("build_totals(course, results, student_totals, gilde, team)")
build_totals(course, results, student_totals, gilde, team_coaches)
# with open("dump.json", 'w') as f:
#     # dict_result = json.dumps(student_totals, indent = 4)
#     json.dump(student_totals, f, indent=2)

if tennant == "inno":
    # with open("dump.json", 'w') as f:
    #     # dict_result = json.dumps(student_totals, indent = 4)
    #     json.dump(student_totals, f, indent=2)
    print("build_late(results, student_totals)")
    build_late(results, student_totals)

plot_totals(course, student_totals, read_progress(start.progress_file_name), gilde, team_coaches, labels_colors)

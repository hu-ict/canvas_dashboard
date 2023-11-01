import json
from lib.build_totals import build_totals
from lib.build_bootstrap import build_bootstrap_general
from lib.build_late import build_late
from lib.lib_plotly import peil_labels
from lib.plot_totals import plot_totals
from lib.file import read_course, read_start, read_results, read_progress


def init_roles_list():
    role_list = {}
    for role in course.roles:
        role_list[role.short] = []
    return role_list


def init_roles_dict():
    role_list = {}
    for role in course.roles:
        role_list[role.short] = {}
    return role_list


def init_roles_count():
    role_count = {}
    for role in course.roles:
        role_count[role.short] = 0
    return role_count


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


def init_coaches_dict():
    team_list = {}
    for teacher in course.teachers:
        if len(teacher.projects) > 0:
            team_list[teacher.initials] = {}
    return team_list


start = read_start()
course = read_course(start.course_file_name)
results = read_results(start.results_file_name)
actual_day = (results.actual_date - course.start_date).days

peilen = {}
for peil in peil_labels:
    peilen[peil] = {
            'overall': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'team': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'gilde': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'kennis': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
        }

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

gilde = init_roles_dict()
team = init_coaches_dict()

print("build_bootstrap(course, results)")
build_bootstrap_general(course, results)

print("build_totals(course, results, student_totals, gilde, team)")
build_totals(course, results, student_totals, gilde, team)
with open("dump.json", 'w') as f:
    # dict_result = json.dumps(student_totals, indent = 4)
    json.dump(student_totals, f, indent=2)

print("plot_totals(course, student_totals, read_progress('''progress_sep23.json'''), gilde, team)")
plot_totals(course, student_totals, read_progress("progress_sep23.json"), gilde, team)

print("build_late(results, student_totals)")
build_late(results, student_totals)

from lib.build_totals import build_totals
from lib.build_bootstrap import build_bootstrap_general
from lib.build_late import build_late
from lib.config import peil_labels
from lib.plot_totals import plot_totals
from lib.file import read_course, read_start, read_results


def get_gilde_count():
    gilde_count = {}
    for role in course.roles:
        gilde_list[role.short] = []
        gilde_count[role.short] = 0
    return gilde_count


def get_coaches_count():
    team_coaches_count = {}
    for teacher in course.teachers:
        if len(teacher.projects) > 0:
            team_coaches_list[teacher.initials] = []
            team_coaches_count[teacher.initials] = 0
    return team_coaches_count


course_config_start = read_start()
course = read_course(course_config_start.course_file_name)
results = read_results(course_config_start.results_file_name)
actual_day = (results.actual_date - course_config_start.start_date).days
team_coaches_list = {}
gilde_list = {}

peilen = {}
for peil in peil_labels:
    peilen[peil] = {
            'overall': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'team': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'gilde': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'kennis': {-1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
        }

student_totals = {
    'student_count': 0,
    'team': {'count': [], 'pending': get_coaches_count(), 'late': get_coaches_count(), 'to_late': get_coaches_count(), 'list': team_coaches_list,},
    'gilde': {'count': [], 'pending': get_gilde_count(), 'late': get_gilde_count(), 'to_late': get_gilde_count()},
    'kennis': {'count': [], 'pending': get_gilde_count(), 'late': get_gilde_count(), 'to_late': get_gilde_count()},
    'peil': peilen,
    'late': {'count': []}
}

submissions_late = {
    'team': team_coaches_list,
    'gilde': gilde_list,
    'kennis': gilde_list
}

print("build_bootstrap(course_config_start, course, results)")
build_bootstrap_general(course_config_start, course, results)

print("build_totals(results, student_totals, submissions_late)")
build_totals(results, student_totals, submissions_late)

print("plot_totals(course_config_start, course, student_totals)")
plot_totals(course_config_start, course, student_totals)

print("build_late(course_config_start.course_id, submissions_late)")
build_late(course_config_start.course_id, submissions_late)

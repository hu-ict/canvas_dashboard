from lib.build_totals import build_totals
from lib.build_bootstrap import build_bootstrap
from lib.build_late import build_late
from lib.config import peil_labels
from lib.plot_totals import plot_totals
from lib.file import read_course, read_start, read_results

course_config_start = read_start()
course = read_course(course_config_start.course_file_name)
results = read_results(course_config_start.results_file_name)

actual_day = (results.actual_date - course_config_start.start_date).days

team_coaches_list = {}
team_coaches_count = {}
for teacher in course.teachers:
    if len(teacher.projects) > 0:
        team_coaches_list[teacher.initials] = []
        team_coaches_count[teacher.initials] = 0

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
    'team': {'count': [], 'pending': team_coaches_count, 'late': team_coaches_count, 'to_late': team_coaches_count, 'list': team_coaches_list,},
    'gilde': {'count': [], 'pending': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}, 'late': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}, 'to_late': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}},
    'kennis': {'count': [], 'pending': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}, 'late': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}, 'to_late': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}},
    'peil': peilen,
    'late': {'count': []}
}

print(student_totals)
submissions_late = {
    'team': team_coaches_list,
    'gilde': {'AI': [], 'BIM': [], 'CSC': [], 'SD_B': [], 'SD_F': [], 'TI': []},
    'kennis': {'AI': [], 'BIM': [], 'CSC': [], 'SD_B': [], 'SD_F': [], 'TI': []}
}

print("build_bootstrap(course_config_start, course, results)")
build_bootstrap(course_config_start, course, results)

print("build_totals(results, student_totals, submissions_late)")
build_totals(results, student_totals, submissions_late)

print("plot_totals(course_config_start, course, student_totals)")
plot_totals(course_config_start, course, student_totals)

print("build_late(course_config_start.course_id, submissions_late)")
build_late(course_config_start.course_id, submissions_late)

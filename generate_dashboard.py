import json
import sys

from lib.build_totals import build_totals
from lib.build_bootstrap import build_bootstrap_general
from lib.build_late import build_late_list
from lib.lib_date import get_actual_date
from lib.plot_totals import plot_werkvoorraad, plot_voortgang
from lib.file import read_course, read_start, read_results, read_progress, read_levels, read_course_instance, read_workload
from model.WorkloadDay import WorkloadDay


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


def init_coaches_count(coaches):
    team_count = {}
    for coach in coaches.values():
        team_count[coach["teacher"].initials] = 0
    return team_count


def init_coaches_list(coaches):
    team_list = {}
    for coach in coaches.values():
        team_list[coach["teacher"].initials] = []
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


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GD02 - Instance:", instances.current_instance, instances.get_category(instances.current_instance))
    start = read_start(instances.get_start_file_name())

    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    level_series = read_levels("levels.json")

    team_coaches = init_coaches_dict(course)
    for team_coach in team_coaches.values():
        print("GD04 -", team_coach["teacher"])

    if instances.is_instance_of("inno_courses"):
        peilen = {}
        for peil in course.level_moments.moments:
            peilen[peil] = {
                'overall': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
                'team': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
                'gilde': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
                'kennis': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
            }
        student_totals = {
            'student_count': 0,
            'perspectives': {
                'team': {'count': [], 'pending': init_coaches_count(team_coaches), 'late': init_coaches_count(team_coaches), 'to_late': init_coaches_count(team_coaches), 'list': init_coaches_list(team_coaches)},
                'gilde': {'count': [], 'pending': init_roles_count(course), 'late': init_roles_count(course), 'to_late': init_roles_count(course), 'list': init_roles_list(course)},
                'kennis': {'count': [], 'pending': init_roles_count(course), 'late': init_roles_count(course), 'to_late': init_roles_count(course), 'list': init_roles_list(course)}
            },
            'level_moments': peilen,
            'actual_progress': {
                'overall': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
                'team': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
                'gilde': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
                'kennis': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
            },
            'late': {'count': []}
        }
    elif instances.is_instance_of("prop_courses"):
        student_totals = {
            'student_count': 0,
            'perspectives': {},
            'level_moments': None,
            'late': {'count': []}
        }
        for perspective in course.perspectives.keys():
            student_totals["perspectives"][perspective] = {'count': [], 'pending': init_sections_count(course), 'late': init_sections_count(course), 'to_late': init_sections_count(course), 'list': init_sections_list(course)}
        if course.level_moments is not None:
            student_totals["level_moments"] = {}
            for moment in course.level_moments.moments:
                student_totals["level_moments"][moment] = {'overall': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}}
                for perspective in course.perspectives.keys():
                    student_totals["level_moments"][moment][perspective] = {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
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
            student_totals['perspectives'][perspective] = {'count': [], 'pending': init_sections_count(course), 'late': init_sections_count(course), 'to_late': init_sections_count(course), 'list': init_sections_list(course)}

    with open("student_totals.json", 'w') as f:
        dict_result = student_totals
        json.dump(dict_result, f, indent=2)


    # with open("dump.json", 'w') as f:
    #     dict_result = json.dumps(student_totals, indent = 4)
    #     json.dump(student_totals, f, indent=2)

    # print("GD04", student_totals)
    print("GD05 - build_totals(start, course, results, student_totals, gilde, team_coaches)")
    build_totals(instances, start, course, results, student_totals)
    print("GD06 - build_bootstrap_general(start, course, results, team_coaches, labels_colors)")
    build_bootstrap_general(instances, start, course, results, team_coaches, level_series, student_totals)


    print("GD07 - build_late(instances, start, results, student_totals)")
    build_late_list(instances, start, results, student_totals)
    with open("student_totals.json", 'w') as f:
        dict_result = student_totals
        json.dump(dict_result, f, indent=2)

    workload_history = read_workload(instances.get_workload_file_name(instances.current_instance))
    workload_day = WorkloadDay(results.actual_day)
    workload_day.from_late_list(student_totals["late"]["count"])
    workload_history.append_day(workload_day)

    with open(instances.get_workload_file_name(instances.current_instance), 'w') as f:
        dict_result = workload_history.to_json()
        json.dump(dict_result, f, indent=2)

    plot_werkvoorraad(instances, start, course, student_totals, workload_history)
    plot_voortgang(instances, course, student_totals, read_progress(instances.get_progress_file_name(instances.current_instance)), level_series.level_series['progress'])
    print("GD99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GD01 - generate_dashboard.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

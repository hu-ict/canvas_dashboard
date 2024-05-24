import json
import sys

from lib.build_totals import build_totals
from lib.build_bootstrap import build_bootstrap_general
from lib.build_late import build_late_list
from lib.lib_date import get_actual_date
from lib.lib_plotly import peil_labels
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


def init_coaches_count(course):
    team_count = {}
    for teacher in course.teachers:
        if len(teacher.projects) > 0:
            team_count[teacher.initials] = 0
    return team_count


def init_coaches_list(course):
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


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance, instances.get_category(instances.current_instance))
    start = read_start(instances.get_start_file_name())

    course = read_course(start.course_file_name)
    results = read_results(start.results_file_name)
    levels = read_levels("levels.json")

    # if start.progress_perspective:
    peilen = {}
    for peil in peil_labels:
        peilen[peil] = {
            'overall': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'team': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'gilde': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0},
            'kennis': {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0, 3: 0}
        }

    if instances.is_instance_of("inno_courses") or instances.is_instance_of("inno_courses_new"):
        student_totals = {
            'student_count': 0,
            'perspectives': {
                'team': {'count': [], 'pending': init_coaches_count(course), 'late': init_coaches_count(course), 'to_late': init_coaches_count(course), 'list': init_coaches_list(course)},
                'gilde': {'count': [], 'pending': init_roles_count(course), 'late': init_roles_count(course), 'to_late': init_roles_count(course), 'list': init_roles_list(course)},
                'kennis': {'count': [], 'pending': init_roles_count(course), 'late': init_roles_count(course), 'to_late': init_roles_count(course), 'list': init_roles_list(course)}
            },
            'progress': peilen,
            'late': {'count': []}
        }
    else:
        student_totals = {
            'student_count': 0,
            'perspectives': {},
            'progress': peilen,
            'late': {'count': []}
        }
        for perspective in course.perspectives:
            student_totals['perspectives'][perspective] = {'count': [], 'pending': init_sections_count(course), 'late': init_sections_count(course), 'to_late': init_sections_count(course), 'list': init_sections_list(course)}

    team_coaches = init_coaches_dict(course)
    # with open("dump.json", 'w') as f:
    #     dict_result = json.dumps(student_totals, indent = 4)
    #     json.dump(student_totals, f, indent=2)

    print(student_totals)
    print("build_totals(start, course, results, student_totals, gilde, team_coaches)")
    build_totals(instances, start, course, results, student_totals)
    print("build_bootstrap_general(start, course, results, team_coaches, labels_colors)")
    build_bootstrap_general(instances, start, course, results, team_coaches, levels, student_totals)

    if instances.is_instance_of("inno_courses") or instances.is_instance_of("inno_courses_new"):
        # with open("dump.json", 'w') as f:
        #     # dict_result = json.dumps(student_totals, indent = 4)
        #     json.dump(student_totals, f, indent=2)
        print("build_late(start, results, student_totals)")
        build_late_list(instances, start, results, student_totals)

    workload_history = read_workload(start.workload_file_name)
    workload_day = WorkloadDay(results.actual_day)
    workload_day.from_late_list(student_totals["late"]["count"])
    workload_history.append_day(workload_day)

    with open(start.workload_file_name, 'w') as f:
        dict_result = workload_history.to_json()
        json.dump(dict_result, f, indent=2)

    plot_werkvoorraad(instances, start, course, student_totals, workload_history, levels)
    plot_voortgang(instances, start, course, student_totals, read_progress(start.progress_file_name), levels)
    print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("generate_dashboard.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

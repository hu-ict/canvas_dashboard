import json
import sys

from lib.build_bootstrap import build_bootstrap_general
from lib.build_bootstrap_structure import build_bootstrap_structure_index
from lib.lib_date import get_actual_date
from lib.file import read_course, read_start, read_levels, read_course_instance


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
    print("GS02 - Instance:", instances.current_instance, instances.get_category(instances.current_instance))
    start = read_start(instances.get_start_file_name())

    course = read_course(instances.get_course_file_name(instances.current_instance))
    level_series = read_levels("levels.json")

    team_coaches = init_coaches_dict(course)
    for team_coach in team_coaches.values():
        print("GS04 -", team_coach["teacher"])

    print("GS06 - build_bootstrap_structure_index(start, course, team_coaches, level_series)")
    build_bootstrap_structure_index(instances, start, course, team_coaches, level_series)

    print("GS99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GS01 - generate_structure.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

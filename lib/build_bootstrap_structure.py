from string import Template

from lib.build_bootstrap_release_planning import build_bootstrap_release_planning_tab
from lib.build_plotly_analyse import process_analyse
from lib.build_plotly_bandwidth import process_bandwidth
from lib.file import read_plotly
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_date_time_loc


def build_learning_analytics(course, results, level_serie_collection):
    learning_analytics = {}
    for assignment_group in course.assignment_groups:
        perspective = course.find_perspective_by_assignment_group(assignment_group.id)
        if perspective is not None:
            grades = level_serie_collection.level_series[perspective.levels].grades
            for assignment_sequence in assignment_group.assignment_sequences:
                for assignment in assignment_sequence.assignments:
                    grades_dict = {}
                    for grade in grades.keys():
                        grades_dict[grade] = 0
                    learning_analytics[str(assignment.id)] = {"assignment": assignment.id,
                                                              "assignment_name": assignment.name,
                                                              "level_serie": perspective.levels,
                                                              "status": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
                                                              "grades": grades_dict}

    for student in results.students:
        # print(l_peil_construction)
        # print("GL10 -", student.name)
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    learning_analytics[str(submission.assignment_id)]["status"][str(submission.status)] += 1
                    if submission.grade is not None:
                        learning_analytics[str(submission.assignment_id)]["grades"][str(submission.grade)] += 1
        for submission in student.student_level_moments.submissions:
            learning_analytics[str(submission.assignment_id)]["status"][str(submission.status)] += 1
            if submission.grade is not None:
                print("BLA02 -", submission.assignment_name, submission.assignment_id, submission.grade)
                learning_analytics[str(submission.assignment_id)]["grades"][str(submission.grade)] += 1
        for submission in student.student_grade_moments.submissions:
            learning_analytics[str(submission.assignment_id)]["status"][str(submission.status)] += 1
            if submission.grade is not None:
                print("BLA03 -", submission.assignment_name, submission.assignment_id, submission.grade)
                learning_analytics[str(submission.assignment_id)]["grades"][str(submission.grade)] += 1
    return learning_analytics


def build_student_button(course, student, templates, labels_colors):
    role = course.get_role(student.role)
    if not role:
        return ""
    color = role.btn_color
    l_progress_color = labels_colors.level_series['progress'].levels["-1"].color
    return templates['student'].substitute(
        {'btn_color': color, 'progress_color': l_progress_color, 'student_name': student.name,
         'student_role': role.name, 'student_file': "asci_file_name"})


def build_bootstrap_canvas_overzicht(a_templates, a_perspectives, a_student_totals):
    overzicht_html_string = ""
    for perspective in a_perspectives:
        list_html_string = ""
        for selector in a_student_totals["perspectives"][perspective.name]["list"].keys():
            # print(selector)
            list_html_string += a_templates["selector"].substitute(
                {'selector_file': "late_" + perspective.name + "_" + selector + ".html", 'selector': selector})
        overzicht_html_string += a_templates["overzicht"].substitute(
            {'perspective': perspective.title, 'buttons': list_html_string})
    return overzicht_html_string


def build_bootstrap_group(a_course, a_templates, a_labels_colors):
    # coaches = {}
    groups_html_string = ''
    for group in a_course.student_groups:
        # print(group.name, len(group.students))
        students_html_string = ''
        coaches_string = ""
        if len(group.teachers) > 0:
            coaches = ""
            for coach in group.teachers:
                teacher = a_course.find_teacher(coach)
                coaches += " " + str(teacher.id)
                coaches_string += ", " + teacher.name
        else:
            coaches = None
        for student in group.students:
            l_student = a_course.find_student(student.id)
            students_html_string += build_student_button(a_course, l_student, a_templates, a_labels_colors)
        if coaches:
            group_html_string = a_templates['group'].substitute(
                {'selector_type': 'coach', 'selector': coaches, 'student_group_name': group.name + coaches_string,
                 'students': students_html_string})
        else:
            group_html_string = a_templates['group'].substitute(
                {'selector_type': 'coach', 'selector': 'leeg', 'student_group_name': group.name + coaches_string,
                 'students': students_html_string})

        groups_html_string += group_html_string

    return groups_html_string


def build_bootstrap_role(a_course, a_templates, a_labels_colors):
    roles_html_string = ''
    for role in a_course.roles:
        students_html_string = ''
        for student in role.students:
            l_student = a_course.find_student(student.id)
            students_html_string += build_student_button(a_course, l_student, a_templates, a_labels_colors)
        titel = role.name + ", " + str(len(role.students)) + " studenten"
        role_html_string = a_templates['group'].substitute(
            {'selector_type': 'role_view', 'selector': role.short, 'student_group_name': titel,
             'students': students_html_string})
        roles_html_string += role_html_string
    return roles_html_string


def build_bootstrap_progress(a_start, a_course, a_results, a_templates, a_labels_colors):
    progress_html_string = ''
    for level in a_labels_colors.level_series['progress'].levels:
        students_html_string = ''
        for student in a_results.students:
            if str(student.progress) == str(level):
                students_html_string += build_student_button(a_start, a_course, student, a_templates, a_labels_colors)
        titel = a_labels_colors.level_series['progress'].levels[level].label + ", " + " studenten"
        level_html_string = a_templates['group'].substitute(
            {'selector_type': 'progress_view', 'selector': 'level', 'student_group_name': titel,
             'students': students_html_string})
        progress_html_string += level_html_string
    return progress_html_string


def build_bootstrap_analyse_tab(instance, a_course, learning_analytics, a_templates, a_level_serie_collection, actual_day):
    html_string = ""
    for assignment_group in a_course.assignment_groups:
        assignment_html_string = ""
        assignment_list = []
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                assignment_list.append(assignment)
        assignment_list = sorted(assignment_list, key=lambda a: a.assignment_day)
        for assignment in assignment_list:
            file_name = instance.name + "/general/analyse_" + str(assignment.id) + ".html"
            if assignment.assignment_day < actual_day:
                background_color = "#ffb3b3"
            else:
                background_color = "#c6ecd9"
            assignment_html_string += a_templates["analyse_assignment"].substitute(
                {'url': file_name,
                 'assignment_name': assignment.name,
                 'background_color': background_color,
                 'assignment_lock_date': get_date_time_loc(
                     assignment.assignment_date)})
            process_analyse(learning_analytics, assignment, a_level_serie_collection,
                            instance.get_html_root_path() + file_name)

        html_string += a_templates["analyse_card"].substitute({'assignment_group_id': str(assignment_group.id),
                                                               'assignment_group_name': assignment_group.name,
                                                               'assignments': assignment_html_string})
    return html_string


def build_bootstrap_tabs(a_instance, a_start, a_course, a_templates, a_labels_colors):
    tabs = ["Groepen"]
    if len(a_course.roles) > 1:
        tabs.append("Rollen")
    tabs.append("Release Planning")
    html_tabs = ""
    for tab in tabs:
        if tab == "Groepen":
            students_html_string = build_bootstrap_group(a_course, a_templates, a_labels_colors)
        elif tab == "Rollen":
            students_html_string = build_bootstrap_role(a_course, a_templates, a_labels_colors)
        elif tab == "Release Planning":
            students_html_string = build_bootstrap_release_planning_tab(a_instance, a_start, a_course, a_templates,
                                                                        a_labels_colors)
        else:
            pass
        html_tab = ""
        for tab1 in tabs:
            if tab == tab1:
                html_tab += a_templates['students_tab'].substitute({'tab': tab1, 'active': 'active', 'aria': 'page'})
            else:
                html_tab += a_templates['students_tab'].substitute({'tab': tab1, 'active': '', 'aria': 'false'})
        html_tabs += a_templates['students_tabs'].substitute(
            {'tab': tab, 'tabs': html_tab, 'students': students_html_string})
    return html_tabs


def get_initials(item):
    return item[1].initials


def build_bootstrap_structure_index(a_instances, a_start, a_course, a_coaches, a_labels_colors):
    l_templates = load_templates(a_instances.get_template_path())
    tabs_html_string = build_bootstrap_tabs(a_instances, a_start, a_course, l_templates, a_labels_colors)

    coaches_html_string = ''
    for coach in a_coaches.values():
        coaches_html_string += l_templates["coach"].substitute(
            {'coach_name': coach['teacher'].name, 'coach_initials': coach['teacher'].initials,
             'coach_id': coach['teacher'].id})

    roles_string = ""
    for role in a_course.roles:
        roles_string += l_templates['role'].substitute(
            {'button': role.btn_color, 'role': role.short})

    if len(a_course.roles) > 1:
        roles_card_html_string = l_templates['roles_card'].substitute({'roles': roles_string, 'colums': '3'})
        coaches_card_html_string = l_templates['coaches_card'].substitute(
            {'coaches': coaches_html_string, 'colums': '3'})
    else:
        roles_card_html_string = ""
        coaches_card_html_string = l_templates['coaches_card'].substitute(
            {'coaches': coaches_html_string, 'colums': '8'})

    index_html_string = l_templates['index_structure'].substitute(
        {'course_name': a_course.name, 'aantal_studenten': a_course.student_count,
         'aantal_teams': len(a_course.student_groups),
         'roles_card': roles_card_html_string,
         'coaches_card': coaches_card_html_string,
         'tabs_html_string': tabs_html_string})

    with open(a_instances.get_html_path() + 'index_structure.html', mode='w', encoding="utf-8") as file_index:
        print("BS89 - Schrijf stucture HTML:", a_instances.get_html_path() + 'index_structure.html')
        file_index.write(index_html_string)

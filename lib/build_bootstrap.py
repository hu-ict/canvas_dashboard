from lib.build_bootstrap_learning_outcome import build_bootstrap_learning_outcome_tab
from lib.build_bootstrap_structure import build_bootstrap_analytics_tab, build_learning_analytics, \
    build_bootstrap_release_planning_tab, build_bootstrap_analyse_tab
from lib.build_bootstrap_werkvoorraad import build_bootstrap_canvas_werkvoorraad_tab
from lib.lib_date import get_date_time_loc


def build_student_button(instance, role, student, templates, level_serie_collection):
    color = role.btn_color
    student_name = student.email.split("@")[0].lower()
    index_file_name = ".//" + instance.name + "//students//" + student_name + "_index.html"
    # print("BB21 -", level_serie_collection.level_series['progress'].grades, str(student.progress))
    if student.progress >= 0:
        l_progress_color = level_serie_collection.level_series['progress'].grades[str(student.progress)].color
    else:
        l_progress_color = level_serie_collection.level_series['progress'].grades[str(0)].color
    return templates['student'].substitute(
        {'btn_color': color,
         'progress_color': l_progress_color,
         'student_name': student.name,
         'student_number': student.number,
         'student_role': role.name,
         'frame_right': index_file_name
         })


def build_bootstrap_group(a_instance, a_course, a_student_groups, a_results, a_templates, level_series):
    # coaches = {}
    groups_html_string = ''
    for group in a_student_groups:
        # print(group.name, len(group.students))
        students_html_string = ""
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
            l_student = a_results.find_student(student.id)
            if l_student is None:
                print("BB05 - ERROR Student not found in results", student, "re-run generate_results")
            else:
                # print('BB07 -', l_student.name, "[", l_student.number, "]")
                role = a_course.get_role(l_student.role)
                if role is not None:
                    students_html_string += build_student_button(a_instance, role, l_student, a_templates, level_series)
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


def build_bootstrap_role(a_instance, a_course, a_results, a_templates, level_series):
    roles_html_string = ''
    for role in a_course.roles:
        students_html_string = ''
        for student in role.students:
            l_student = a_results.find_student(student.id)
            if l_student is None:
                print("BB11 - Student niet gevonden in resultaten", student)
            else:
                students_html_string += build_student_button(a_instance, role, l_student, a_templates, level_series)
        titel = role.name + ", " + str(len(role.students)) + " studenten"
        role_html_string = a_templates['group'].substitute(
            {'selector_type': 'role_view', 'selector': role.short, 'student_group_name': titel,
             'students': students_html_string})
        roles_html_string += role_html_string
    return roles_html_string


def build_bootstrap_progress(a_instance, a_course, a_results, a_templates, level_serie_collection):
    progress_html_string = ''
    for level in level_serie_collection.level_series['progress'].grades:
        students_html_string = ''
        for student in a_results.students:
            if str(student.progress) == str(level):
                role = a_course.get_role(student.role)
                if role is not None:
                    students_html_string += build_student_button(a_instance, role, student, a_templates, level_serie_collection)
        titel = level_serie_collection.level_series['progress'].grades[level].label + ", " + " studenten"
        level_html_string = a_templates['group'].substitute(
            {'selector_type': 'progress_view', 'selector': 'level', 'student_group_name': titel,
             'students': students_html_string})
        progress_html_string += level_html_string
    return progress_html_string


def write_release_planning(a_start, a_templates, a_assignment_group, a_file_name):
    list_html_string = ""
    for assignment in a_assignment_group.assignments:
        url = "https://canvas.hu.nl/courses/" + str(a_start.canvas_course_id) + "/assignments/" + str(assignment.id)
        # print(assignment.name)
        rubric_points = 0
        rubric_count = 0
        for criterion in assignment.rubrics:
            rubric_points += criterion.points
            rubric_count += 1
        if rubric_count == 0:
            rubrics_str = "Geen criteria"
        else:
            rubrics_str = str(int(rubric_points)) + " [" + str(rubric_count) + "]"
        list_html_string += a_templates["assignment"].substitute({'assignment_name': assignment.name,
                                                                  'assignment_unlock_date': get_date_time_loc(
                                                                      assignment.unlock_date),
                                                                  'assignment_lock_date': get_date_time_loc(
                                                                      assignment.assignment_date),
                                                                  'assignment_grading_type': assignment.grading_type,
                                                                  'assignment_points': assignment.points,
                                                                  'rubrics_points': rubrics_str,
                                                                  'url': url})
    file_html_string = a_templates["release_planning_list"].substitute(
        {'total_points': int(a_assignment_group.total_points), 'lower_points': a_assignment_group.lower_points,
         'upper_points': a_assignment_group.upper_points, 'strategie': a_assignment_group.strategy,
         'assignments': list_html_string})

    with open(a_file_name, mode='w', encoding="utf-8") as file_list:
        file_list.write(file_html_string)


def build_bootstrap_students_tabs(a_instance, a_course, a_results, a_templates, a_level_serie_collection, a_total_workload):
    tabs = ["Groepen"]
    if len(a_course.guild_groups) > 0:
        tabs.append("Gilden")
    if len(a_course.roles) > 1:
        tabs.append("Rollen")
    tabs.append("Voortgang")
    tabs.append("Werkvoorraad")
    tabs.append("Release Planning")
    tabs.append("Leeruitkomsten")
    tabs.append("Analytics")
    if a_instance.is_instance_of("inno_courses") or a_instance.is_instance_of("inno_courses_2026"):
        tabs.append("Analyse")
    start_pages = {}
    start_pages["Groepen"] = "./" + a_instance.name + "/general/standard.html"
    start_pages["Gilden"] = "./" + a_instance.name + "/general/standard.html"
    start_pages["Rollen"] = "./" + a_instance.name + "/general/standard.html"
    start_pages["Voortgang"] = "./" + a_instance.name + "/general/totals_voortgang.html"
    start_pages["Werkvoorraad"] = "./" + a_instance.name + "/general/workload_index.html"
    start_pages["Release Planning"] = "./" + a_instance.name + "/general/standard.html"
    start_pages["Leeruitkomsten"] = "./" + a_instance.name + "/general/standard.html"
    start_pages["Analytics"] = "./" + a_instance.name + "/general/standard.html"
    start_pages["Analyse"] = "./" + a_instance.name + "/general/standard.html"
    html_tabs = ""
    for tab in tabs:
        if tab == "Groepen":
            print("BB51 - Tab groepen")
            tabs_html_string = build_bootstrap_group(a_instance, a_course, a_course.project_groups, a_results, a_templates, a_level_serie_collection)
        elif tab == "Gilden":
            print("BB52 - Tab gilden")
            tabs_html_string = build_bootstrap_group(a_instance, a_course, a_course.guild_groups, a_results, a_templates, a_level_serie_collection)
        elif tab == "Rollen":
            print("BB53 - Tab rollen")
            tabs_html_string = build_bootstrap_role(a_instance, a_course, a_results, a_templates, a_level_serie_collection)
        elif tab == "Voortgang":
            print("BB54 - Tab voortgang")
            tabs_html_string = build_bootstrap_progress(a_instance, a_course, a_results, a_templates, a_level_serie_collection)
        elif tab == "Werkvoorraad":
            print("BB55 - Tab werkvoorrad")
            perspectives = []
            for perspective in a_course.perspectives.values():
                perspectives.append(perspective)
            if a_course.level_moments is not None:
                perspectives.append(a_course.level_moments)
            if a_course.grade_moments is not None:
                perspectives.append(a_course.grade_moments)
            tabs_html_string = build_bootstrap_canvas_werkvoorraad_tab(a_instance, a_templates, a_course, perspectives,
                                                                   a_total_workload)
        elif tab == "Release Planning":
            print("BB56 - Tab release planning")
            tabs_html_string = build_bootstrap_release_planning_tab(a_instance, a_course, a_templates,
                                                                    a_level_serie_collection)
        elif tab == "Leeruitkomsten":
            print("BB57 - Tab leeruitkomsten")
            tabs_html_string = build_bootstrap_learning_outcome_tab(a_instance, a_course, a_templates,
                                                                    a_level_serie_collection)
        elif tab == "Analytics":
            print("BB58 - Tab learning_analytics")
            learning_analytics = build_learning_analytics(a_course, a_results, a_level_serie_collection)
            tabs_html_string = build_bootstrap_analytics_tab(a_instance, a_course, learning_analytics, a_templates,
                                                       a_level_serie_collection, a_results.actual_day)
        else:
            print("BB59 - Tab analyse peil/beoordeling")
            tabs_html_string = build_bootstrap_analyse_tab(a_instance, a_course, a_results, a_templates,
                                                       a_level_serie_collection)
        html_tab = ""
        for tab1 in tabs:
            file_name = start_pages[tab1]
            if tab == tab1:
                html_tab += a_templates['index_tab'].substitute(
                    {'tab': tab1, 'active': 'active', 'aria': 'page', 'selector_file': file_name})
            else:
                html_tab += a_templates['index_tab'].substitute(
                    {'tab': tab1, 'active': '', 'aria': 'false', 'selector_file': file_name})
        html_tabs += a_templates['index_tabs'].substitute(
            {'tab': tab, 'tabs': html_tab, 'content': tabs_html_string})
    return html_tabs


def get_initials(item):
    return item[1].initials


def build_bootstrap_general(a_instance, a_course, a_results, a_templates, a_teachers, level_series, a_total_workload):
    l_semester_day = a_results.actual_day
    tabs_html_string = build_bootstrap_students_tabs(a_instance, a_course, a_results, a_templates, level_series,
                                                     a_total_workload)
    teacher_html_string = ''
    for teacher in a_teachers.values():
        teacher_html_string += a_templates["coach"].substitute(
            {'coach_name': teacher['teacher'].name, 'coach_id': teacher['teacher'].id,
             'coach_initials': teacher['teacher'].initials})

    roles_string = ""
    for role in a_course.roles:
        roles_string += a_templates['role'].substitute(
            {'button': role.btn_color, 'role': role.short})
    percentage = str(l_semester_day / a_course.days_in_semester * 100) + "%"
    actual_date_str = a_results.actual_date.strftime("%d-%m-%Y %H:%M")

    if len(a_course.roles) > 1:
        roles_card_html_string = a_templates['roles_card'].substitute({'roles': roles_string, 'colums': '3'})
        coaches_card_html_string = a_templates['coaches_card'].substitute(
            {'coaches': teacher_html_string, 'colums': '3'})
    else:
        roles_card_html_string = ""
        coaches_card_html_string = a_templates['coaches_card'].substitute(
            {'coaches': teacher_html_string, 'colums': '6'})

    index_html_string = a_templates['index'].substitute(
        {'course_name': a_course.name, 'aantal_studenten': a_course.student_count,
         'aantal_teams': len(a_course.project_groups),
         'submission_count': a_results.submission_count, 'not_graded_count': a_results.not_graded_count,
         'actual_date': actual_date_str, 'semester_day': l_semester_day,
         'percentage': percentage,
         'roles_card': roles_card_html_string,
         'coaches_card': coaches_card_html_string,
         'tabs_html_string': tabs_html_string})

    with open(a_instance.get_html_root_path() + 'index.html', mode='w', encoding="utf-8") as file_index:
        file_index.write(index_html_string)

    standard_html_string = a_templates['standard'].substitute({})
    with open(a_instance.get_html_path() + 'standard.html', mode='w', encoding="utf-8") as file_index:
        file_index.write(standard_html_string)

from scripts.lib.build_bootstrap_analyse import build_bootstrap_analyse_tab
from scripts.lib.build_bootstrap_learning_analytics import build_learning_analytics, \
    build_bootstrap_learning_analytics_tab
from scripts.lib.build_bootstrap_learning_outcome import build_bootstrap_learning_outcome_tab
from scripts.lib.build_bootstrap_release_planning import build_bootstrap_release_planning_tab

from scripts.lib.build_bootstrap_werkvoorraad import build_bootstrap_teacher_tab, WORKLOAD_PLOTLY_HTML
from scripts.lib.plot_totals import RELEASE_PLANNING_PLOTLY_HTML, PROGRESS_PLOTLY_HTML


def build_student_button(instance, role, student, templates, level_serie_collection):
    color = role.btn_color
    student_name = student.email.split("@")[0].lower()
    index_file_name = instance.get_link_student_path() + student_name + "_index.html"
    # print("BBDI25 -", level_serie_collection.level_series['progress'].grades, str(student.progress))
    if student.progress >= 0:
        l_progress_color = level_serie_collection.level_series['progress'].grades[str(student.progress)].color
    else:
        l_progress_color = level_serie_collection.level_series['progress'].grades[str(-1)].color
    bof_count = 0
    for learning_outcome in student.learning_outcomes.values():
        bof_count += len(learning_outcome.feedback_list)
    return templates['student'].substitute(
        {'btn_color': color,
         'progress_color': l_progress_color,
         'student_name': student.name,
         'student_number': student.number,
         'student_role': role.name,
         'bof_count': bof_count,
         'frame_right': index_file_name
         })


def build_bootstrap_groups(a_instance, a_course, a_student_groups, a_results, a_templates, level_series, group_type):
    # coaches = {}
    html_string = ''
    for group in a_student_groups:
        # print("BBDI05 -", group.name, len(group.assessors))
        students_html_string = ""
        if group.principal_assessor > 0:
            assessor = a_course.find_teacher(group.principal_assessor)
            if assessor is not None:
                assessors_string = assessor.name
            else:
                assessors_string = ""
                print("BBDI07 - teacher_id not found:", assessor.teacher_id)
        else:
            assessors_string = ""
        print("BBDI08 -", group.principal_assessor,  assessors_string)
        coaches = ""
        for assessor in group.assessors:
            coaches += " "+str(assessor.teacher_id)

        for student in group.students:
            l_student = a_results.find_student(student.id)
            if l_student is None:
                print("BBDI08 - ERROR Student not found in results", student, "re-run generate_results")
            else:
                # print('BB07 -', l_student.name, "[", l_student.number, "]")
                role = a_course.get_role(l_student.role)
                if role is not None:
                    students_html_string += build_student_button(a_instance, role, l_student, a_templates, level_series)
                else:
                    print("BBDI21 - role for student is NoneType", l_student)
        if len(coaches) > 0:
            group_html_string = a_templates['group'].substitute(
                {'selector_type': 'coach', 'selector': coaches, 'student_group_name': group.name + ", " + assessors_string,
                 'students': students_html_string})
        else:
            group_html_string = a_templates['group'].substitute(
                {'selector_type': 'coach', 'selector': 'leeg', 'student_group_name': group.name,
                 'students': students_html_string})
        html_string += group_html_string
    return html_string


def build_bootstrap_role(a_instance, a_course, a_results, a_templates, level_series):
    html_string = ''
    for role in a_course.roles:
        students_html_string = ''
        for student in role.students:
            l_student = a_results.find_student(student.id)
            if l_student is None:
                print("BBDI11 - Student niet gevonden in resultaten", student)
            else:
                students_html_string += build_student_button(a_instance, role, l_student, a_templates, level_series)
        titel = role.name + ", " + str(len(role.students)) + " studenten"
        role_html_string = a_templates['group'].substitute(
            {'selector_type': 'role_view', 'selector': role.short, 'student_group_name': titel,
             'students': students_html_string})
        html_string += role_html_string
    return html_string


def build_bootstrap_progress(a_instance, a_course, a_results, a_templates, level_serie_collection):
    html_string = ''
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
        html_string += level_html_string

    return html_string


def build_bootstrap_menu_html(a_instance, a_templates, menu_items):
    start_pages = {}
    for menu_item in menu_items:
        if menu_item == "groups":
            start_pages[menu_item] = a_instance.get_link_general_path() + "standard.html"
        elif menu_item == "guilds":
            start_pages[menu_item] = a_instance.get_link_general_path() + "standard.html"
        elif menu_item == "roles":
            start_pages[menu_item] = a_instance.get_link_general_path() + "standard.html"
        elif menu_item == "levels":
            start_pages[menu_item] = a_instance.get_link_general_path() + PROGRESS_PLOTLY_HTML
        elif menu_item == "workload":
            start_pages[menu_item] = a_instance.get_link_general_path() + WORKLOAD_PLOTLY_HTML
        elif menu_item == "learning_outcomes":
            start_pages[menu_item] = a_instance.get_link_general_path() + "standard.html"
        elif menu_item == "release_planning":
            start_pages[menu_item] = a_instance.get_link_general_path() + RELEASE_PLANNING_PLOTLY_HTML
        elif menu_item == "learning_analytics":
            start_pages[menu_item] = a_instance.get_link_general_path() + "standard.html"
        elif menu_item == "analytics":
            start_pages[menu_item] = a_instance.get_link_general_path() + "standard.html"
        else:
            pass
    html_menu_string = ""
    for tab in menu_items:
        html_menu = ""
        for tab1 in menu_items:
            file_name = start_pages[tab1]
            if tab == tab1:
                html_menu += a_templates['index_tab'].substitute(
                    {'tab': tab1, 'tab_label': menu_items[tab1], 'active': 'active', 'aria': 'page', 'selector_file': file_name})
            else:
                html_menu += a_templates['index_tab'].substitute(
                    {'tab': tab1, 'tab_label': menu_items[tab1], 'active': '', 'aria': 'false', 'selector_file': file_name})
        html_menu_string += a_templates['index_menu'].substitute({'tab': tab, 'menu': html_menu})
    return html_menu_string


def build_bootstrap_left_panel_html(a_instance, a_menu_items, a_course, a_results, a_templates, a_level_serie_collection, a_workload):
    html_tabs = ""
    for tab in a_menu_items:
        if tab == "groups":
            print("BBDI51 - Tab", tab)
            tabs_html_string = build_bootstrap_groups(a_instance, a_course, a_course.project_groups, a_results, a_templates, a_level_serie_collection, "PROJECT")
        elif tab == "guilds":
            print("BBDI52 - Tab", tab)
            tabs_html_string = build_bootstrap_groups(a_instance, a_course, a_course.guild_groups, a_results, a_templates, a_level_serie_collection, "GUILD")
        elif tab == "roles":
            print("BBDI53 - Tab", tab)
            tabs_html_string = build_bootstrap_role(a_instance, a_course, a_results, a_templates, a_level_serie_collection)
        elif tab == "levels":
            print("BBDI54 - Tab", tab)
            tabs_html_string = build_bootstrap_progress(a_instance, a_course, a_results, a_templates, a_level_serie_collection)
        elif tab == "workload":
            print("BBDI55 - Tab", tab)
            tabs_html_string = build_bootstrap_teacher_tab(a_instance, a_templates, a_workload)
        elif tab == "release_planning":
            print("BBDI56 - Tab", tab)
            tabs_html_string = build_bootstrap_release_planning_tab(a_instance, a_course, a_templates,
                                                                    a_level_serie_collection)
        elif tab == "learning_outcomes":
            print("BBDI57 - Tab", tab)
            tabs_html_string = build_bootstrap_learning_outcome_tab(a_instance, a_course, a_templates,
                                                                    a_level_serie_collection)
        elif tab == "learning_analytics":
            print("BBDI58 - Tab", tab)
            learning_analytics = build_learning_analytics(a_course, a_results, a_level_serie_collection)
            tabs_html_string = build_bootstrap_learning_analytics_tab(a_instance, a_course, learning_analytics, a_templates,
                                                       a_level_serie_collection, a_results.actual_day)
        elif tab == "analytics":
            print("BBDI59 - Tab", tab)
            tabs_html_string = build_bootstrap_analyse_tab(a_instance, a_course, a_results, a_templates,
                                                       a_level_serie_collection)
        else:
            print("BBDI60 - Unknown Tab", tab)
        html_tab = ""
        html_tabs += a_templates['index_tabs'].substitute(
            {'tab': tab, 'tabs': html_tab, 'content': tabs_html_string})
    return html_tabs


def get_initials(item):
    return item[1].initials


def build_bootstrap_dashboard_index(a_instance, a_course, a_results, a_templates, a_teachers, dashboard, a_total_workload):
    l_semester_day = a_results.actual_day
    menu_html_string = build_bootstrap_menu_html(a_instance, a_templates, dashboard.dashboard_tabs)
    print("BBDI71 - menu_html_string", len(menu_html_string))
    left_panel_html_string = build_bootstrap_left_panel_html(a_instance, dashboard.dashboard_tabs, a_course, a_results, a_templates, dashboard.level_serie_collection, a_total_workload)
    print("BBDI72 - left_panel_html_string", len(left_panel_html_string))
    teacher_html_string = ''
    for teacher in a_teachers:
        teacher_html_string += a_templates["coach"].substitute(
            {'teacher_name': teacher.name, 'teacher_id': teacher.id,
             'teacher_initials': teacher.initials})

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
         'menu_html_string': menu_html_string,
         'left_panel_html_string': left_panel_html_string})

    with open(a_instance.get_html_index_path() + 'index.html', mode='w', encoding="utf-8") as file_index:
        file_index.write(index_html_string)

    standard_html_string = a_templates['standard'].substitute({})
    with open(a_instance.get_html_general_path() + 'standard.html', mode='w', encoding="utf-8") as file_index:
        file_index.write(standard_html_string)

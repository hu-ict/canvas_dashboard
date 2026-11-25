
from scripts.lib.build_bootstrap_learning_analytics import build_learning_analytics_dict, \
    build_bootstrap_learning_analytics_tab
from scripts.lib.build_bootstrap_learning_outcome import build_bootstrap_learning_outcome_tab
from scripts.lib.build_bootstrap_release_planning import build_bootstrap_release_planning_tab
from scripts.lib.build_bootstrap_saturation import build_bootstrap_saturation_tab
from scripts.lib.build_bootstrap_student_button import build_student_button

from scripts.lib.build_bootstrap_werkvoorraad import build_bootstrap_workload_tab, WORKLOAD_PLOTLY
from scripts.lib.plot_totals import RELEASE_PLANNING_PLOTLY_HTML, PROGRESS_PLOTLY_HTML, SATURATION_PLOTLY_HTML


def build_bootstrap_groups(a_instance, a_course, a_student_groups, a_results, a_templates, level_serie_collection):
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
        # print("BBDI08 -", group.principal_assessor,  assessors_string)
        coaches = ""
        for assessor in group.assessors:
            coaches += " "+str(assessor.teacher_id)

        for student in group.students:
            result_student = a_results.find_student(student.id)
            if result_student is None:
                print("BBDI09 - ERROR Student not found in results", student, "re-run generate_results")
            else:
                # print('BB07 -', l_student.name, "[", l_student.number, "]")
                role = a_course.get_role(result_student.role)
                if role is not None:
                    student_name = result_student.email.split("@")[0].lower()
                    url = a_instance.get_link_student_path() + student_name + "_index.html"
                    students_html_string += build_student_button(role.btn_color, result_student, "frame_right", url, a_templates, level_serie_collection)
                else:
                    print("BBDI21 - role for student is NoneType", result_student)
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


def build_bootstrap_role(a_instance, a_course, a_results, a_templates, level_serie_collection):
    html_string = ''
    for role in a_course.roles:
        students_html_string = ''
        for student in role.students:
            l_student = a_results.find_student(student.id)
            if l_student is None:
                print("BBDI11 - Student niet gevonden in resultaten", student)
            else:
                student_name = l_student.email.split("@")[0].lower()
                url = a_instance.get_link_student_path() + student_name + "_index.html"
                students_html_string += build_student_button(role.btn_color, l_student, "frame_right", url, a_templates,
                                                             level_serie_collection)
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
        for l_student in a_results.students:
            if str(l_student.progress) == str(level):
                role = a_course.get_role(l_student.role)
                if role is not None:
                    student_name = l_student.email.split("@")[0].lower()
                    url = a_instance.get_link_student_path() + student_name + "_index.html"
                    students_html_string += build_student_button(role.btn_color, l_student, "frame_right", url,
                                                                 a_templates,
                                                                 level_serie_collection)
        titel = level_serie_collection.level_series['progress'].grades[level].label + ", " + " studenten"
        level_html_string = a_templates['group'].substitute(
            {'selector_type': 'progress_view', 'selector': 'level', 'student_group_name': titel,
             'students': students_html_string})
        html_string += level_html_string

    return html_string


def build_bootstrap_menu_html(a_instance, a_templates, menu_items):
    start_pages = {}
    for menu_item in menu_items:
        if menu_item == "groups_1":
            start_pages[menu_item] = a_instance.get_link_general_path() + "standard.html"
        elif menu_item == "groups_2":
            start_pages[menu_item] = a_instance.get_link_general_path() + "standard.html"
        elif menu_item == "roles":
            start_pages[menu_item] = a_instance.get_link_general_path() + "standard.html"
        elif menu_item == "levels":
            start_pages[menu_item] = a_instance.get_link_general_path() + PROGRESS_PLOTLY_HTML
        elif menu_item == "saturation":
            start_pages[menu_item] = a_instance.get_link_general_path() + "portfolio_item_saturation.html"
        elif menu_item == "workload":
            start_pages[menu_item] = a_instance.get_link_general_path() + WORKLOAD_PLOTLY + "_teachers.html"
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
        if tab == "groups_1":
            print("BBDI51 - Tab", tab)
            tabs_html_string = build_bootstrap_groups(a_instance, a_course, a_course.groups_1, a_results, a_templates, a_level_serie_collection)
        elif tab == "groups_2":
            print("BBDI52 - Tab", tab)
            tabs_html_string = build_bootstrap_groups(a_instance, a_course, a_course.groups_2, a_results, a_templates, a_level_serie_collection)
        elif tab == "roles":
            print("BBDI53 - Tab", tab)
            tabs_html_string = build_bootstrap_role(a_instance, a_course, a_results, a_templates, a_level_serie_collection)
        elif tab == "levels":
            print("BBDI54 - Tab", tab)
            tabs_html_string = build_bootstrap_progress(a_instance, a_course, a_results, a_templates, a_level_serie_collection)
        elif tab == "saturation":
            print("BBDI57 - Tab", tab)
            tabs_html_string = build_bootstrap_saturation_tab(a_instance, a_course, a_templates, a_level_serie_collection)
        elif tab == "workload":
            print("BBDI55 - Tab", tab)
            tabs_html_string = build_bootstrap_workload_tab(a_instance, a_templates, a_workload)
        elif tab == "release_planning":
            print("BBDI56 - Tab", tab)
            tabs_html_string = build_bootstrap_release_planning_tab(a_instance, a_course, a_templates, a_level_serie_collection)
        elif tab == "learning_outcomes":
            print("BBDI57 - Tab", tab)
            tabs_html_string = build_bootstrap_learning_outcome_tab(a_instance, a_course, a_templates, a_level_serie_collection)
        elif tab == "learning_analytics":
            print("BBDI58 - Tab", tab)
            learning_analytics = build_learning_analytics_dict(a_course, a_results, a_level_serie_collection)
            tabs_html_string = build_bootstrap_learning_analytics_tab(a_instance, a_course, a_results, learning_analytics, a_templates, a_level_serie_collection, a_results.actual_day)
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
    for tab in dashboard.dashboard_tabs:
        if tab == "groups_1":
            dashboard.dashboard_tabs[tab] = dashboard.groups_1.title
        if tab == "groups_2":
            dashboard.dashboard_tabs[tab] = dashboard.groups_2.title
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
         'aantal_teams': len(a_course.groups_1),
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

from string import Template

from lib.build_bootstrap_structure import build_bootstrap_release_planning
from lib.lib_bootstrap import load_templates
from lib.lib_date import get_date_time_obj, get_date_time_loc
from lib.translation_table import translation_table
from test_bandwidth import process_bandwidth


def build_student_button(start, course, student, templates, labels_colors):
    role = course.get_role(student.role)
    if not role:
        return ""
    color = role.btn_color
    file_name = "./plotly/" + student.name.replace(" ", "%20") + ".html"
    #       file_name = plot_path + student.name + ".html"
    asci_file_name = file_name.translate(translation_table)
    l_progress_color = labels_colors.level_series['progress'].levels[str(student.progress)].color
    return templates['student'].substitute(
        {'btn_color': color, 'progress_color': l_progress_color, 'student_name': student.name,
         'student_role': role.name, 'student_file': asci_file_name})


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


def build_bootstrap_group(a_start, a_course, a_results, a_templates, a_labels_colors):
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
                coaches += " " + teacher.initials
                coaches_string += ", " + teacher.name
        else:
            coaches = None
        for student in group.students:
            l_student = a_results.find_student(student.id)
            students_html_string += build_student_button(a_start, a_course, l_student, a_templates, a_labels_colors)
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


def build_bootstrap_role(a_start, a_course, a_results, a_templates, a_labels_colors):
    roles_html_string = ''
    for role in a_course.roles:
        students_html_string = ''
        for student in role.students:
            l_student = a_results.find_student(student.id)
            students_html_string += build_student_button(a_start, a_course, l_student, a_templates, a_labels_colors)
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


def build_bootstrap_slb(a_start, a_course, a_results, a_templates, a_labels_colors):
    l_groups_html_string = ''
    for group in a_course.slb_groups:
        # print("-", group.name)
        students_html_string = ''
        for student in group.students:
            l_student = a_results.find_student(student.id)
            students_html_string += build_student_button(a_start, a_course, l_student, a_templates, a_labels_colors)

        group_html_string = a_templates['group'].substitute(
            {'selector_type': 'coach', 'selector': 'Leeg', 'student_group_name': group.name,
             'students': students_html_string})

        l_groups_html_string += group_html_string

    return l_groups_html_string

# build_bootstrap_release_planning

def write_release_planning(a_start, a_templates, a_assignment_group, a_file_name):
    list_html_string = ""
    for assignment in a_assignment_group.assignments:
        url = "https://canvas.hu.nl/courses/" + str(a_start.canvas_course_id) + "/assignments/" + str(assignment.id)
        print(assignment.name)
        rubric_points = 0
        rubric_count = 0
        for criterion in assignment.rubrics:
            rubric_points += criterion.points
            rubric_count += 1
        if rubric_count == 0:
            rubrics_str = "Geen criteria"
        else:
            rubrics_str = str(int(rubric_points))+" ["+str(rubric_count)+"]"
        list_html_string += a_templates["assignment"].substitute({'assignment_name': assignment.name,
                                                                  'assignment_unlock_date': get_date_time_loc(assignment.unlock_date),
                                                                  'assignment_lock_date': get_date_time_loc(assignment.assignment_date),
                                                                  'assignment_grading_type': assignment.grading_type,
                                                                  'assignment_points': assignment.points,
                                                                  'rubrics_points': rubrics_str,
                                                                  'url': url})
    file_html_string = a_templates["release_planning_list"].substitute({'total_points': int(a_assignment_group.total_points), 'lower_points': a_assignment_group.lower_points, 'upper_points': a_assignment_group.upper_points, 'strategie': a_assignment_group.strategy, 'assignments': list_html_string})

    with open(a_file_name, mode='w', encoding="utf-8") as file_list:
        file_list.write(file_html_string)


# def build_bootstrap_release_planning(a_instances, a_start, a_course, a_templates, a_labels_colors):
#     html_string = ""
#     buttons_planning_html_string = ""
#     for assignment_group in a_course.assignment_groups:
#         file_name = "release_planning_" + str(assignment_group.id) + ".html"
#         buttons_planning_html_string += a_templates["selector"].substitute(
#             {'selector_file': file_name,
#              'selector': assignment_group.name}) + "<br>"
#         write_release_planning(a_start, a_templates, assignment_group, a_instances.get_html_path() + file_name)
#
#     buttons_flow_html_string = ""
#     for assignment_group in a_course.assignment_groups:
#         file_name = "bandwidth_" + str(assignment_group.id) + ".html"
#         buttons_flow_html_string += a_templates["selector"].substitute(
#             {'selector_file': file_name,
#              'selector': assignment_group.name}) + "<br>"
#         process_bandwidth(a_instances, a_start, a_course, assignment_group, a_labels_colors)
#
#
#     html_string += a_templates["release_planning"].substitute({'buttons_planning': buttons_planning_html_string, 'buttons_flow': buttons_flow_html_string})
#     return html_string


def build_bootstrap_students_tabs(a_instances, a_start, a_course, a_results, a_templates, a_labels_colors, a_totals):
    tabs = ["Groepen"]
    if len(a_course.roles) > 1:
        tabs.append("Rollen")
    tabs.append("Voortgang")
    if a_start.slb_groep_name:
        tabs.append("SLB")
    tabs.append("Overzichten")
    tabs.append("Release Planning")
    html_tabs = ""
    for tab in tabs:
        if tab == "Groepen":
            students_html_string = build_bootstrap_group(a_start, a_course, a_results, a_templates, a_labels_colors)
        elif tab == "Rollen":
            students_html_string = build_bootstrap_role(a_start, a_course, a_results, a_templates, a_labels_colors)
        elif tab == "Voortgang":
            students_html_string = build_bootstrap_progress(a_start, a_course, a_results, a_templates, a_labels_colors)
        elif tab == "SLB":
            students_html_string = build_bootstrap_slb(a_start, a_course, a_results, a_templates, a_labels_colors)
        elif tab == "Overzichten":
            students_html_string = a_templates['overzichten'].template
            perspectives = []
            for perspective in a_course.perspectives.values():
                perspectives.append(perspective)
            students_html_string += build_bootstrap_canvas_overzicht(a_templates, perspectives, a_totals)
        elif tab == "Release Planning":
            students_html_string = build_bootstrap_release_planning(a_instances, a_start, a_course, a_templates, a_labels_colors)
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


def build_bootstrap_general(a_instances, a_start, a_course, a_results, a_templates, a_coaches, a_labels_colors, a_totals):
    l_semester_day = (a_results.actual_date - a_start.start_date).days
    tabs_html_string = build_bootstrap_students_tabs(a_instances, a_start, a_course, a_results, a_templates, a_labels_colors,
                                                     a_totals)

    coaches_html_string = ''
    for coach in a_coaches.values():
        coaches_html_string += a_templates["coach"].substitute(
            {'coach_name': coach['teacher'].name, 'coach_initials': coach['teacher'].initials})

    roles_string = ""
    for role in a_course.roles:
        roles_string += a_templates['role'].substitute(
            {'button': role.btn_color, 'role': role.short})
    percentage = str(l_semester_day / a_course.days_in_semester * 100) + "%"
    actual_date_str = a_results.actual_date.strftime("%d-%m-%Y %H:%M")

    if len(a_course.roles) > 1:
        roles_card_html_string = a_templates['roles_card'].substitute({'roles': roles_string, 'colums': '3'})
        coaches_card_html_string = a_templates['coaches_card'].substitute(
            {'coaches': coaches_html_string, 'colums': '3'})
    else:
        roles_card_html_string = ""
        coaches_card_html_string = a_templates['coaches_card'].substitute(
            {'coaches': coaches_html_string, 'colums': '6'})

    index_html_string = a_templates['index'].substitute(
        {'course_name': a_course.name, 'aantal_studenten': a_course.student_count,
         'aantal_teams': len(a_course.student_groups),
         'submission_count': a_results.submission_count, 'not_graded_count': a_results.not_graded_count,
         'actual_date': actual_date_str, 'semester_day': l_semester_day,
         'percentage': percentage,
         'roles_card': roles_card_html_string,
         'coaches_card': coaches_card_html_string,
         'tabs_html_string': tabs_html_string})

    with open(a_instances.get_html_path() + 'index.html', mode='w', encoding="utf-8") as file_index:
        file_index.write(index_html_string)

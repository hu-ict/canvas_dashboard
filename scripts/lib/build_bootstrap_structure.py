from scripts.lib.build_bootstrap_release_planning import build_bootstrap_release_planning_tab
from scripts.lib.build_bootstrap_student import get_comments_html
from scripts.lib.build_plotly_analyse import process_analytics
from scripts.lib.lib_bootstrap import load_templates
from scripts.lib.lib_date import get_date_time_loc
from scripts.lib.lib_progress import get_overall_progress
from scripts.model.dashboard.LevelSerie import STR_GRADES
from scripts.model.perspective.Status import NOT_YET_GRADED




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




def process_analyse_level_moment(course, results, level_moment, level_serie_collection, a_templates, a_file_name):
    student_html_string = ""
    for student in results.students:
        level_perspectives = []
        perspectives_html = ""
        for perspective in student.perspectives.values():
            level_moment_submission = student.get_level_moment_submission_by_query([level_moment, perspective.name])
            if level_moment_submission is None:
                level_determined = 0
            else:
                grade = level_moment_submission.grade
                if grade is not None:
                    level_determined = int(grade)
                else:
                    level_determined = 0
            level_perspectives.append(level_determined)
            level_determined_label = level_serie_collection.level_series[course.level_moments.levels].grades[
                str(level_determined)].label
            level_determined_color = level_serie_collection.level_series[course.level_moments.levels].grades[
                str(level_determined)].color
            perspectives_html += '<td style="background-color: '+level_determined_color+';">'+level_determined_label+"</td>"
        # print("BBS21 -", course.level_moments.levels, perspective.progress)
        level_flow_calculated_label = level_serie_collection.level_series[course.level_moments.levels].grades[
            str(perspective.progress)].label.upper()
        overall_level_calculated = get_overall_progress(level_perspectives)
        level_moment_submission = student.get_level_moment_submission_by_query(["student", level_moment])
        if level_moment_submission is not None:
            overall_level_determined = level_moment_submission.grade
            if overall_level_determined is None:
                overall_level_determined = 0
        else:
            overall_level_determined = 0
        overall_level_determined_label = level_serie_collection.level_series[course.level_moments.levels].grades[
            str(overall_level_determined)].label
        overall_level_determined_color = level_serie_collection.level_series[course.level_moments.levels].grades[
            str(overall_level_determined)].color
        # print("PA11 -", course.level_moments.levels, overall_level_calculated, level_perspectives)
        overall_level_calculated_label = level_serie_collection.level_series[course.level_moments.levels].grades[
            str(overall_level_calculated)].label
        overall_level_calculated_color = level_serie_collection.level_series[course.level_moments.levels].grades[
            str(overall_level_calculated)].color
        # file_name = instance.name + "/general/analyse_" + str(level_moment) + ".html"
        if int(overall_level_determined) != int(overall_level_calculated):
            message = f"FOUT {student.name} OVERALL, bepaalde beoordeling {overall_level_determined_label} inconsistent met regels voor berekende beoordeling {overall_level_calculated_label}"
        else:
            message = ""

        student_html_string += a_templates["moment"].substitute(
            {'url': "hoi",
             'student_name': student.name,
             'perspectives': perspectives_html,
             'overall_calculated_label': overall_level_determined_label,
             'overall_determined_label': overall_level_calculated_label,
             'overall_calculated_color': overall_level_determined_color,
             'overall_determined_color': overall_level_calculated_color,
             'message': message})

    perspectives_html = ""
    for perspective in course.perspectives:
        perspectives_html += "<th>" + perspective + "</th>"

    moment_html_string = a_templates["moments_list"].substitute(
            {'url': "hoi",
             'perspectives': perspectives_html,
             'moments': student_html_string})
    with open(a_file_name, mode='w', encoding="utf-8") as file_index:
        print("BS89 - Schrijf momenten HTML:", a_file_name)
        file_index.write(moment_html_string)


def process_analyse_moment(course, results, grade_moment, level_serie_collection, a_templates, a_file_name):
    student_html_string = ""
    for student in results.students:
        student_moment = student.get_grade_moment(grade_moment.id)
        level_serie = level_serie_collection.level_series["grade"]
        moment_grade_comments = get_comments_html(student_moment.comments)
        url = "https://canvas.hu.nl/courses/" + str(course.canvas_id) + "/gradebook/speed_grader?assignment_id=" + str(
            student_moment.assignment.id) + "&student_id=" + str(student_moment.student_id)
        if student_moment.graded:
            if student_moment.grade is not None:
                moment_label = level_serie.grades[student_moment.grade].label
                moment_color = level_serie.grades[student_moment.grade].color
            else:
                moment_label = level_serie.grades["0"].label
                moment_color = level_serie.grades["0"].color
        else:
            # Niet bepaald
            moment_label = level_serie.get_status(NOT_YET_GRADED).label
            moment_color = level_serie.get_status(NOT_YET_GRADED).color

        student_html_string += a_templates["moment"].substitute(
            {'url': url,
             'student_name': student.name,
             'moment_color': moment_color,
             'moment_grade': moment_label,
             'moment_comment': moment_grade_comments})

    moment_html_string = a_templates["moments_list"].substitute(
            {'url': "hoi",
             'moments': student_html_string})
    with open(a_file_name, mode='w', encoding="utf-8") as file_index:
        print("BS89 - Schrijf momenten HTML:", a_file_name)
        file_index.write(moment_html_string)


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

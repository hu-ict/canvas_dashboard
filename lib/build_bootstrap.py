from string import Template

from lib.translation_table import translation_table

def build_student_button(start, course, student, templates, labels_colors):
    role = course.get_role(student.role)
    if not role:
        return ""
    color = role.btn_color
    file_name = "./plotly/" + student.name.replace(" ", "%20") + ".html"
#       file_name = plot_path + student.name + ".html"
    asci_file_name = file_name.translate(translation_table)
    l_progress_color = labels_colors.level_series[start.progress.levels].levels[str(student.progress)].color
    return templates['student'].substitute(
            {'btn_color': color, 'progress_color': l_progress_color, 'student_name': student.name,
            'student_role': role.name, 'student_file': asci_file_name})


def build_bootstrap_overzicht(a_templates, a_student_totals):
    team_html_string = ""

    for selector in a_student_totals["perspectives"]["team"]["list"].keys():
        # print(selector)
        team_html_string += a_templates["selector"].substitute(
            {'selector_file': "late_"+"team"+"_"+selector+".html", 'selector': selector})

    gilde_html_string = ""
    for selector in a_student_totals['perspectives']["gilde"]['list'].keys():
        gilde_html_string += a_templates["selector"].substitute(
            {'selector_file': "late_"+"gilde"+"_"+selector+".html", 'selector': selector})

    kennis_html_string = ""
    for selector in a_student_totals['perspectives']["kennis"]['list'].keys():
        kennis_html_string += a_templates["selector"].substitute(
            {'selector_file': "late_"+"kennis"+"_"+selector+".html", 'selector': selector})

    overzicht_html_string = a_templates["overzicht"].substitute({'team_buttons': team_html_string, 'gilde_buttons': gilde_html_string, 'kennis_buttons': kennis_html_string})
    return overzicht_html_string

def build_bootstrap_project(a_start, a_course, a_results, a_templates, a_labels_colors):
    # coaches = {}
    groups_html_string = ''
    for group in a_course.student_groups:
        print(group.name, len(group.students))
        students_html_string = ''
        coaches_string = ""
        if len(group.teachers) > 0:
            coaches = ""
            for coach in group.teachers:
                teacher = a_course.find_teacher(coach)
                coaches += " "+teacher.initials
                coaches_string += ", "+teacher.name
        else:
            coaches = None
        for student in group.students:
            l_student = a_results.find_student(student.id)
            students_html_string += build_student_button(a_start, a_course, l_student, a_templates, a_labels_colors)
        if coaches:
            group_html_string = a_templates['group'].substitute(
                {'selector_type': 'coach', 'selector': coaches, 'student_group_name': group.name+coaches_string, 'students': students_html_string})
        else:
            group_html_string = a_templates['group'].substitute(
                {'selector_type': 'coach', 'selector': 'leeg', 'student_group_name': group.name+coaches_string, 'students': students_html_string})

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
        role_html_string = a_templates['group'].substitute({'selector_type': 'role_view', 'selector': role.short,  'student_group_name': titel, 'students': students_html_string})
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
        level_html_string = a_templates['group'].substitute({'selector_type': 'progress_view', 'selector': 'level',  'student_group_name': titel, 'students': students_html_string})
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
            {'selector_type': 'coach', 'selector': 'Leeg', 'student_group_name': group.name, 'students': students_html_string})

        l_groups_html_string += group_html_string

    return l_groups_html_string


def load_templates(template_path):
    templates = {}
    # Create a template that has placeholder for value of x
    with open(template_path+'template_overzicht.html', mode='r', encoding="utf-8") as file_late_template:
        string_late_html = file_late_template.read()
        templates["overzicht"] = Template(string_late_html)

    with open(template_path + 'template_slb.html', mode='r', encoding="utf-8") as file_slb_template:
        string_slb_html = file_slb_template.read()
        templates["slb"] = Template(string_slb_html)

    with open(template_path + 'template.html', mode='r', encoding="utf-8") as file_index_template:
        string_index_html = file_index_template.read()
        templates["index"] = Template(string_index_html)

    with open(template_path + 'template_studentgroup.html', mode='r', encoding="utf-8") as file_group_template:
        string_group_html = file_group_template.read()
        templates["group"] = Template(string_group_html)

    with open(template_path + 'template_role_selector.html', mode='r', encoding="utf-8") as file_role_template:
        string_role_html = file_role_template.read()
        templates["role"]  = Template(string_role_html)

    with open(template_path + 'template_student.html', mode='r', encoding="utf-8") as file_student_template:
        string_student_html = file_student_template.read()
        templates["student"] = Template(string_student_html)

    with open(template_path + 'template_coach.html', mode='r', encoding="utf-8") as file_coach_template:
        string_coach_html = file_coach_template.read()
        templates["coach"] = Template(string_coach_html)

    with open(template_path + 'template_selector.html', mode='r', encoding="utf-8") as file_selector_template:
            string_selector_html = file_selector_template.read()
            templates["selector"] = Template(string_selector_html)

    return templates


def get_initials(item):
    return item[1].initials


def build_bootstrap_general(a_instances, a_start, a_course, a_results, a_coaches, a_labels_colors, a_totals):
    l_semester_day = (a_results.actual_date - a_start.start_date).days
    l_templates = load_templates(a_start.template_path)

    student_groups_html_string = build_bootstrap_project(a_start, a_course, a_results, l_templates, a_labels_colors)
    role_groups_html_string = build_bootstrap_role(a_start, a_course, a_results, l_templates, a_labels_colors)
    progress_groups_html_string = build_bootstrap_progress(a_start, a_course, a_results, l_templates, a_labels_colors)
    overicht_html_string = build_bootstrap_overzicht(l_templates, a_totals)

    coaches_html_string = ''
    for coach in a_coaches.values():
        coaches_html_string += l_templates["coach"].substitute(
            {'coach_name': coach['teacher'].name, 'coach_initials': coach['teacher'].initials})

    roles_string = ""
    for role in a_course.roles:
        roles_string += l_templates['role'].substitute(
            {'button': role.btn_color, 'role': role.short})
    percentage = str(l_semester_day / a_course.days_in_semester * 100) + "%"
    actual_date_str = a_results.actual_date.strftime("%d-%m-%Y %H:%M")
    slb_groups_html_string = build_bootstrap_slb(a_start, a_course, a_results, l_templates, a_labels_colors)
    index_html_string = l_templates['index'].substitute(
        {'course_name': a_course.name, 'aantal_studenten': a_course.student_count, 'aantal_teams': len(a_course.student_groups),
         'submission_count': a_results.submission_count, 'not_graded_count': a_results.not_graded_count,
         'actual_date': actual_date_str, 'semester_day': l_semester_day,
         'percentage': percentage,
         'roles': roles_string,
         'coaches': coaches_html_string,
         'student_groups': student_groups_html_string,
         'slb_groups': slb_groups_html_string,
         'role_groups': role_groups_html_string,
         'progress_groups': progress_groups_html_string,
         'overzicht': overicht_html_string})

    with open(a_instances.get_html_path() + 'index.html', mode='w', encoding="utf-8") as file_index:
        file_index.write(index_html_string)




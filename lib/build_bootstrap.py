from string import Template

from lib.build_totals import get_actual_progress
from lib.lib_plotly import score_voortgang_dict, template_path_general
from lib.translation_table import translation_table


def build_bootstrap_project(a_course, a_results, a_templates):
    # coaches = {}
    groups_html_string = ''
    for group in a_course.student_groups:
        students_html_string = ''
        if len(group.teachers) > 0:
            teacher_id = group.teachers[0]
            teacher = a_course.find_teacher(teacher_id)
        else:
            teacher = None

        # print(group.name)
        for student in group.students:
            role = student.role
            role_obj = a_course.get_role(role)
            color = role_obj.btn_color
            file_name = "./plotly/" + student.name.replace(" ", "%20") + ".html"
            #       file_name = plot_path + student.name + ".html"
            asci_file_name = file_name.translate(translation_table)
            l_student = a_results.find_student(student.id)
            l_progress = get_actual_progress(l_student.perspectives)
            l_progress_color = score_voortgang_dict[l_progress]['color']


            student_html_string = a_templates['student'].substitute(
                {'btn_color': color, 'progress_color': l_progress_color, 'student_name': student.name, 'student_role': role_obj.name,
                 'student_file': asci_file_name})
            students_html_string += student_html_string

        if teacher:
            group_html_string = a_templates['group'].substitute(
                {'coach': teacher.initials, 'student_group_name': group.name, 'students': students_html_string})
        else:
            group_html_string = a_templates['group'].substitute(
                {'coach': "Leeg", 'student_group_name': group.name, 'students': students_html_string})

        groups_html_string += group_html_string

    return groups_html_string


def build_bootstrap_slb(a_course, a_templates):
    l_groups_html_string = ''
    for group in a_course.slb_groups:
        # print("-", group.name)
        students_html_string = ''
        for student in group.students:
            # print("--", student.name)
            role = student.role
            role_obj = a_course.get_role(role)
            color = role_obj.btn_color
            file_name = "./plotly/" + student.name.replace(" ", "%20") + ".html"
            #       file_name = plot_path + student.name + ".html"
            asci_file_name = file_name.translate(translation_table)
            l_progress = get_actual_progress(student.perspectives)
            l_progress_color = score_voortgang_dict[l_progress]['color']
            student_html_string = a_templates['student'].substitute(
                {'btn_color': color, 'progress_color': l_progress_color, 'student_name': student.name, 'student_role': role_obj.name,
                 'student_file': asci_file_name})
            students_html_string += student_html_string

        group_html_string = a_templates['group'].substitute(
            {'coach': "Leeg", 'student_group_name': group.name, 'students': students_html_string})

        l_groups_html_string += group_html_string

    return l_groups_html_string


def load_templates():
    templates = {}
    # Create a template that has placeholder for value of x
    with open(template_path_general + 'template_slb.html', mode='r', encoding="utf-8") as file_slb_template:
        string_slb_html = file_slb_template.read()
        templates["slb"] = Template(string_slb_html)

    with open(template_path_general + 'template.html', mode='r', encoding="utf-8") as file_index_template:
        string_index_html = file_index_template.read()
        templates["index"] = Template(string_index_html)

    with open(template_path_general + 'template_studentgroup.html', mode='r', encoding="utf-8") as file_group_template:
        string_group_html = file_group_template.read()
        templates["group"] = Template(string_group_html)

    with open(template_path_general + 'template_role_selector.html', mode='r', encoding="utf-8") as file_role_template:
        string_role_html = file_role_template.read()
        templates["role"]  = Template(string_role_html)

    with open(template_path_general + 'template_student.html', mode='r', encoding="utf-8") as file_student_template:
        string_student_html = file_student_template.read()
        templates["student"] = Template(string_student_html)

    with open(template_path_general + 'template_coach.html', mode='r', encoding="utf-8") as file_coach_template:
        string_coach_html = file_coach_template.read()
        templates["coach"] = Template(string_coach_html)
    return templates


def get_initials(item):
    return item[1].initials


def build_bootstrap_general(a_course_config_start, a_course, a_results):
    l_semester_day = (a_results.actual_date - a_course_config_start.start_date).days
    l_templates = load_templates()

    l_coaches = {}
    for group in a_course.student_groups:
        students_html_string = ''
        if len(group.teachers) > 0:
            teacher_id = group.teachers[0]
            teacher = a_course.find_teacher(teacher_id)
            l_coaches[teacher.id] = teacher
        else:
            teacher = None

    groups_html_string = build_bootstrap_project(a_course, a_results, l_templates)


    def get_initials(item):
        return item[1].initials

    coaches = dict(sorted(l_coaches.items(), key=lambda item: get_initials(item)))

    coaches_html_string = ''
    for coach in coaches.values():
        coaches_html_string += l_templates['coach'].substitute(
            {'coach_name': coach.name, 'coach_initials': coach.initials})

    roles_html_string = ""
    for role in a_course.roles:
        roles_html_string += l_templates['role'].substitute(
            {'button': role.btn_color, 'role': role.short})

    actual_date_str = a_results.actual_date.strftime("%d-%m-%Y %H:%M")
    index_html_string = l_templates['index'].substitute(
        {'course_name': a_course.name, 'aantal_studenten': a_course.student_count, 'aantal_teams': len(a_course.student_groups),
         'submission_count': a_results.submission_count, 'not_graded_count': a_results.not_graded_count,
         'actual_date': actual_date_str, 'semester_day': l_semester_day,
         'percentage': str(l_semester_day / 1.5) + "%",
         'roles': roles_html_string,
         'coaches': coaches_html_string,
         'student_groups': groups_html_string})
    index_path = template_path_general
    with open(index_path + 'index.html', mode='w', encoding="utf-8") as file_index:
        file_index.write(index_html_string)

    groups_html_string = build_bootstrap_slb(a_course, l_templates)
    roles_html_string = ""
    for role in a_course.roles:
        roles_html_string += l_templates['role'].substitute(
            {'button': role.btn_color, 'role': role.short})

    actual_date_str = a_results.actual_date.strftime("%d-%m-%Y %H:%M")
    slb_html_string = l_templates['slb'].substitute(
        {'course_name': a_course.name, 'aantal_studenten': a_course.student_count, 'aantal_teams': len(a_course.student_groups),
         'submission_count': a_results.submission_count, 'not_graded_count': a_results.not_graded_count,
         'actual_date': actual_date_str, 'semester_day': l_semester_day,
         'percentage': str(l_semester_day / 1.5) + "%",
         'roles': roles_html_string,
         'student_groups': groups_html_string})
    index_path = template_path_general
    with open(index_path + 'index_slb.html', mode='w', encoding="utf-8") as file_index:
        file_index.write(slb_html_string)

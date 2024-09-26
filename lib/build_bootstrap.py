from lib.build_bootstrap_structure import build_bootstrap_release_planning
from lib.lib_date import get_date_time_loc
from lib.translation_table import translation_table


def build_student_button(course, student, templates, labels_colors):
    role = course.get_role(student.role)
    if not role:
        return ""
    color = role.btn_color
    index_file_name = "./students/" + student.name.replace(" ", "%20") + "%20index.html"
    index_asci_file_name = index_file_name.translate(translation_table)
    l_progress_color = labels_colors.level_series['progress'].levels[str(student.progress)].color
    return templates['student'].substitute(
        {'btn_color': color,
         'progress_color': l_progress_color,
         'student_name': student.name,
         'student_number': student.number,
         'student_role': role.name,
         'frame_right': index_asci_file_name
        })


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


def build_bootstrap_role(a_course, a_results, a_templates, a_labels_colors):
    roles_html_string = ''
    for role in a_course.roles:
        students_html_string = ''
        for student in role.students:
            l_student = a_results.find_student(student.id)
            if l_student is None:
                print("BB11 - Student niet gevonden in resultaten", student)
            else:
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
                students_html_string += build_student_button(a_course, student, a_templates, a_labels_colors)
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
            students_html_string += build_student_button(a_course, l_student, a_templates, a_labels_colors)

        group_html_string = a_templates['group'].substitute(
            {'selector_type': 'coach', 'selector': 'Leeg', 'student_group_name': group.name,
             'students': students_html_string})

        l_groups_html_string += group_html_string

    return l_groups_html_string


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


def build_bootstrap_portfolio(instances, course, student, actual_date, templates, a_levels):
    portfolio_items_html_string = ""
    portfolio_items = []
    learning_outcome_summary = {}
    for learning_outcome in course.learning_outcomes:
        learning_outcome_summary[learning_outcome.id] = {
            'behaalde_punten': 0,
            'complete_items': 0,
            'incomplete_items': 0,
            'niet_gemaakt': 0,
            'niet_beoordeeld': 0
        }
    for perspective in course.perspectives.values():
        for assignment_group_id in perspective.assignment_groups:
            assignment_groep = course.find_assignment_group(assignment_group_id)
            for assignment_sequence in assignment_groep.assignment_sequences:
                portfolio_item = assignment_sequence.name + " (" + str(len(assignment_sequence.assignments)) + ")"
                submission_sequence = student.get_submission_sequence_by_name(assignment_sequence.name)
                student_group = course.find_student_group(student.group_id)
                teacher_str = ""
                for teacher in student_group.teachers:
                    teacher = course.find_teacher(teacher)
                    teacher_str += teacher.name + ", "

                if submission_sequence is not None:
                    if submission_sequence.is_graded():
                        score = submission_sequence.get_score()
                        for learning_outcome_id in assignment_sequence.learning_outcomes:
                            learning_outcome_summary[learning_outcome_id]['behaalde_punten'] += score
                        if score == 0:
                            status = "Niet zichtbaar"
                            cell_status = "status_missed"
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_summary[learning_outcome_id]['niet_gemaakt'] += 1
                        elif score == submission_sequence.points:
                            status = "Voldaan"
                            cell_status = "status_complete"
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_summary[learning_outcome_id]['complete_items'] += 1
                        else:
                            status = "Niet voldaan"
                            cell_status = "status_incomplete"
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_summary[learning_outcome_id]['incomplete_items'] += 1
                    else:
                        status = "Nog niet beoordeeld"
                        cell_status = "status_pending"
                        for learning_outcome_id in assignment_sequence.learning_outcomes:
                            if "Modderman" in student.name:
                                print("BB71 -", learning_outcome_id, assignment_sequence.name)
                            learning_outcome_summary[learning_outcome_id]['niet_beoordeeld'] += 1
                else:
                    status = "Toekomst"
                    cell_status = "status_comming"
                item_dict = {
                    "portfolio_item": portfolio_item,
                    "portfolio_date": get_date_time_loc(assignment_sequence.get_date()),
                    "portfolio_day": assignment_sequence.get_day(),
                    "portfolio_status": status,
                    "cell_status": cell_status
                }
                learning_outcomes_row_html_string = ""
                for learning_outcome in course.learning_outcomes:
                    if learning_outcome.id in assignment_sequence.learning_outcomes:
                        learning_outcomes_row_html_string += '<td style="text-align:center;">V</td>'
                    else:
                        learning_outcomes_row_html_string += '<td></td>'
                item_dict["learning_outcomes"] = learning_outcomes_row_html_string
                portfolio_items.append(item_dict)
    portfolio_items = sorted(portfolio_items, key=lambda p: p['portfolio_day'])
    learning_outcomes_header_html_string = ""
    behaalde_punten_html = ""
    complete_items_html = ""
    incomplete_items_html = ""
    niet_gemaakt_html = ""
    niet_beoordeeld_html = ""

    for learning_outcome in course.learning_outcomes:
        learning_outcomes_header_html_string += '<th scope = "col" >'+learning_outcome.id+'</th>'
        behaalde_punten_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['behaalde_punten'])+"</td>"
        complete_items_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['complete_items'])+"</td>"
        incomplete_items_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['incomplete_items'])+"</td>"
        niet_gemaakt_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['niet_gemaakt'])+"</td>"
        niet_beoordeeld_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['niet_beoordeeld'])+"</td>"

    for portfolio_item in portfolio_items:
        # print(portfolio_item)
        portfolio_items_html_string += templates['learning_outcome'].substitute(portfolio_item)


    student_group = course.find_student_group(student.group_id)
    portfolio_html_string = templates['portfolio'].substitute(
        {'semester': course.name,
         'student_name': student.name,
         'student_email': student.email,
         'student_number': student.number,
         'student_group': student_group.name,
         'teachers': teacher_str,
         'actual_date': get_date_time_loc(actual_date),
         'behaalde_punten': behaalde_punten_html,
         'complete_items': complete_items_html,
         'incomplete_items': incomplete_items_html,
         'niet_gemaakt': niet_gemaakt_html,
         'niet_beoordeeld': niet_beoordeeld_html,
         'learning_outcomes': learning_outcomes_header_html_string,
         'portfolio_items': portfolio_items_html_string})
    file_name = instances.get_student_path() + student.name + " portfolio"
    asci_file_name = file_name.translate(translation_table)
    # print("BB21 - Write portfolio for", student.name)
    with open(asci_file_name + ".html", mode='w', encoding="utf-8") as file_portfolio:
        file_portfolio.write(portfolio_html_string)
    return

def build_bootstrap_student_index(instances, course, student, actual_date, templates, a_levels):
    student_group = course.find_student_group(student.group_id)
    teacher_str = ""
    for teacher in student_group.teachers:
        teacher = course.find_teacher(teacher)
        teacher_str += teacher.name + ", "

    progress_file_name = ".//" + student.name.replace(" ", "%20") + "%20progress.html"
    portfolio_file_name = ".//" + student.name.replace(" ", "%20") + "%20portfolio.html"
    progress_asci_file_name = progress_file_name.translate(translation_table)
    portfolio_asci_file_name = portfolio_file_name.translate(translation_table)
    print("BB91 - Index", progress_file_name, portfolio_asci_file_name)
    student_group = course.find_student_group(student.group_id)
    portfolio_html_string = templates['student_index'].substitute(
        {
            'semester': course.name,
            'student_name': student.name,
            'student_email': student.email,
            'student_number': student.number,
            'student_group': student_group.name,
            'teachers': teacher_str,
            'actual_date': get_date_time_loc(actual_date),
            'progress_file': progress_asci_file_name,
            'portfolio_file': portfolio_asci_file_name
        }
    )
    file_name = instances.get_student_path() + student.name + " index"
    asci_file_name = file_name.translate(translation_table)
    # print("BB21 - Write portfolio for", student.name)
    with open(asci_file_name + ".html", mode='w', encoding="utf-8") as file_portfolio:
        file_portfolio.write(portfolio_html_string)
    return

def build_bootstrap_students_tabs(a_instances, a_start, a_course, a_results, a_templates, a_labels_colors, a_totals):
    tabs = ["Groepen"]
    if len(a_course.roles) > 1:
        tabs.append("Rollen")
    tabs.append("Voortgang")
    # if a_start.slb_groep_name:
    #     tabs.append("SLB")
    tabs.append("Overzichten")
    tabs.append("Release Planning")
    html_tabs = ""
    for tab in tabs:
        if tab == "Groepen":
            students_html_string = build_bootstrap_group(a_start, a_course, a_results, a_templates, a_labels_colors)
        elif tab == "Rollen":
            students_html_string = build_bootstrap_role(a_course, a_results, a_templates, a_labels_colors)
        elif tab == "Voortgang":
            students_html_string = build_bootstrap_progress(a_start, a_course, a_results, a_templates, a_labels_colors)
        # elif tab == "SLB":
        #     students_html_string = build_bootstrap_slb(a_start, a_course, a_results, a_templates, a_labels_colors)
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
    l_semester_day = a_results.actual_day
    tabs_html_string = build_bootstrap_students_tabs(a_instances, a_start, a_course, a_results, a_templates, a_labels_colors,
                                                     a_totals)

    coaches_html_string = ''
    for coach in a_coaches.values():
        coaches_html_string += a_templates["coach"].substitute(
            {'coach_name': coach['teacher'].name, 'coach_id': coach['teacher'].id, 'coach_initials': coach['teacher'].initials})

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

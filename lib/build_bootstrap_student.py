import textwrap

from lib.build_plotly_hover import get_hover_comments
from lib.file import read_plotly
from lib.lib_date import get_date_time_loc
from lib.translation_table import translation_table

def get_comments(comments):
    comments_html_string = ""
    if len(comments) > 0:
        for comment in comments:
            comments_html_string += comment.author_name + " - <i>" + comment.comment + "</i><br>"
    return comments_html_string


def build_student_tabs(instances, course, student_tabs):
    if instances.is_instance_of("inno_courses"):
        tabs = {"voortgang": "Voortgang",
                }
    else:
        tabs = {
            "portfolio": "Portfolio",
            "voortgang": "Voortgang",
            }

    for level_moment in course.level_moments.moments:
        tabs[level_moment.replace(" ", "_").lower()] = level_moment
    tabs_html_string = ""
    for tab in tabs:
        if tab == "portfolio":
            tabs_html_string += '<div class="student_view ' + tab + '"><ul class="nav nav-tabs">\n'
        else:
            tabs_html_string += '<div style="display: None" class="student_view '+tab+'"><ul class="nav nav-tabs">\n'
        for tab_inner in tabs:
            if tab == tab_inner:
                active = "active"
                page = "page"
            else:
                active = ""
                page = "false"
            inner_tab = "'"+tab_inner+"'"
            tabs_html_string += '<li class="nav-item"><a onclick="setStudentView('+inner_tab+')" class="nav-link '+active+'" aria-current="'+page+'" href="#">'+tabs[tab_inner]+'</a></li>\n'
        tabs_html_string += '</ul></div>'
    for tab in tabs:
        tabs_html_string += '<div class="student_view '+tab+'">'
        tabs_html_string += student_tabs[tab]
        tabs_html_string += '</div>\n'
    return tabs_html_string


def build_level_moments(instances, course_id, course, student, templates, levels):
    student_tabs_html_string = {}
    for level_moment in course.level_moments.moments:
        assignment = course.get_level_moments_by_query(level_moment)
        level_moment_submission = student.get_peilmoment_submission_by_query(level_moment)
        print("BLM01 -", level_moment, level_moment_submission)
        if level_moment_submission is None:
            progress_label = levels.level_series[course.level_moments.levels].levels["-1"].label
            progress_color = levels.level_series[course.level_moments.levels].levels["-1"].color
            comments = "Leeg"
            level_moment_html_string = templates['level_moment'].substitute(
                {'level_moment_title': level_moment,
                 'url':  "",
                 'progress_label': progress_label,
                 'progress_color': progress_color,
                 'submitted_date': "Leeg",
                 'grader_name': "leeg",
                 'graded_date': "Leeg",
                 'comments': comments,
                 'body': "Geen reflectie"
                 }
            )
        else:
            comments = get_comments(level_moment_submission.comments)
            url = "https://canvas.hu.nl/courses/" + str(course_id) + "/gradebook/speed_grader?assignment_id=" + str(
                level_moment_submission.assignment_id) + "&student_id=" + str(level_moment_submission.student_id)
            if level_moment_submission.graded:
                progress_label = levels.level_series[course.level_moments.levels].levels[str(int(level_moment_submission.score))].label
                progress_color = levels.level_series[course.level_moments.levels].levels[str(int(level_moment_submission.score))].color
            else:
                # Niet bepaald
                progress_label = levels.level_series[course.level_moments.levels].levels["-1"].label
                progress_color = levels.level_series[course.level_moments.levels].levels["-1"].color
            if level_moment_submission.body == "":
                level_moment_submission.body = "Geen reflectie ingeleverd."
            level_moment_html_string = templates['level_moment'].substitute(
                {'level_moment_title': level_moment_submission.assignment_name,
                 'url': url,
                 'progress_color': progress_color,
                 'progress_label': progress_label,
                 'submitted_date': get_date_time_loc(level_moment_submission.submitted_date),
                 'grader_name': level_moment_submission.grader_name,
                 'graded_date': get_date_time_loc(level_moment_submission.graded_date),
                 'comments': comments,
                 'body': level_moment_submission.body
                 }
            )

        student_tabs_html_string[level_moment.replace(" ", "_").lower()] = level_moment_html_string
        print("BLM09 -", student_tabs_html_string)
    return student_tabs_html_string


def build_bootstrap_portfolio(instances, course_id, course, student, actual_date, templates, level_series):
    portfolio_items_html_string = ""
    portfolio_items = []
    learning_outcome_summary = {}
    for learning_outcome in course.learning_outcomes:
        learning_outcome_summary[learning_outcome.id] = {
            'total_points': 0,
            'status_complete': 0,
            'status_incomplete': 0,
            'status_missed': 0,
            'status_pending': 0
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
                link = ""
                if submission_sequence is not None:
                    if submission_sequence.is_graded():
                        score = submission_sequence.get_score()
                        if score == 0: #"Niet zichtbaar"
                            status = level_series.level_series["bin2"].levels["0"].label
                            cell_status = "status_missed"
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_summary[learning_outcome_id][cell_status] += 1
                        elif score == submission_sequence.points:
                            #portfolio items moet compleet zijn
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_summary[learning_outcome_id]['total_points'] += score
                            status = level_series.level_series["bin2"].levels["2"].label
                            cell_status = "status_complete"
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_summary[learning_outcome_id][cell_status] += 1
                        else: #Niet voldaan
                            status = level_series.level_series["bin2"].levels["1"].label
                            cell_status = "status_incomplete"
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_summary[learning_outcome_id][cell_status] += 1
                    else: #Nog niet beoordeeld
                        status = level_series.level_series["bin2"].levels["-2"].label
                        cell_status = "status_pending"
                        for learning_outcome_id in assignment_sequence.learning_outcomes:
                            learning_outcome_summary[learning_outcome_id][cell_status] += 1
                    teller = 0
                    for submission in submission_sequence.submissions:
                        teller += 1
                        url = "https://canvas.hu.nl/courses/" + str(
                            course_id) + "/gradebook/speed_grader?assignment_id=" + str(
                            submission.assignment_id) + "&student_id=" + str(submission.student_id)
                        link = '<a class="badge '+cell_status+'" target="_blank" href="'+url+'">'+str(teller)+'</a>'
                else:
                    status = level_series.level_series["bin2"].levels["-1"].label
                    cell_status = "status_comming"


                item_dict = {
                    "portfolio_item": portfolio_item,
                    "item_url": link,
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
        # behaalde_punten_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['total_points'])+"</td>"
        complete_items_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['status_complete'])+" ("+str(learning_outcome_summary[learning_outcome.id]['total_points'])+")</td>"
        incomplete_items_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['status_incomplete'])+"</td>"
        niet_gemaakt_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['status_missed'])+"</td>"
        niet_beoordeeld_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['status_pending'])+"</td>"

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
         'attendance_essential_count': str(int(student.attendance_perspective.essential_count)),
         'attendance_count': str(int(student.attendance_perspective.count)),
         'attendance_essential_percentage': str(int(student.attendance_perspective.essential_percentage*100)),
         'attendance_percentage': str(int(student.attendance_perspective.percentage*100)),
         'portfolio_items': portfolio_items_html_string,
         'jquery_inject': "" #'''$(function () {$('[data-toggle="popover"]').popover()})''',
         }
    )
    # file_name = instances.get_student_path() + student.name + " portfolio"
    # asci_file_name = file_name.translate(translation_table)
    # # print("BB21 - Write portfolio for", student.name)
    # with open(asci_file_name + ".html", mode='w', encoding="utf-8") as file_portfolio:
    #     file_portfolio.write(portfolio_html_string)
    return portfolio_html_string

def build_bootstrap_portfolio_empty(instances, course, student, actual_date, templates, level_series):
    portfolio_html_string = templates['portfolio_leeg'].substitute(
        {'student_name': student.name,
         'student_number': student.number,
         })
    file_name = instances.get_student_path() + student.name + " portfolio"
    asci_file_name = file_name.translate(translation_table)
    # print("BB21 - Write portfolio for", student.name)
    with open(asci_file_name + ".html", mode='w', encoding="utf-8") as file_portfolio:
        file_portfolio.write(portfolio_html_string)
    return portfolio_html_string


def build_bootstrap_student_index(instances, course_id, course, student, actual_date, templates, levels):
    student_group = course.find_student_group(student.group_id)
    teacher_str = ""
    for teacher in student_group.teachers:
        teacher = course.find_teacher(teacher)
        teacher_str += teacher.name + ", "
    # progress_file_name = ".//" + student.name.replace(" ", "%20") + "%20progress.html"
    # progress_asci_file_name = progress_file_name.translate(translation_table)
    # # print("BB91 - Index", progress_file_name, portfolio_asci_file_name)
    student_group = course.find_student_group(student.group_id)
    student_tabs = build_level_moments(instances, course_id, course, student, templates, levels)

    if instances.is_instance_of("prop_courses"):
        student_tabs['portfolio'] = build_bootstrap_portfolio(instances, course_id, course, student, actual_date, templates, levels)

    file_name = instances.get_student_path() + student.name + " progress.html"
    asci_file_name = file_name.translate(translation_table)
    student_tabs['voortgang'] = '<h2 class="mt-2">Voortgang</h2>'+read_plotly(asci_file_name)
    print("BSI10 - ", student_tabs.keys())
    student_tabs_html_string = build_student_tabs(instances, course, student_tabs)
    student_index_html_string = templates['student_index'].substitute(
        {
            'semester': course.name,
            'student_name': student.name,
            'student_email': student.email,
            'student_number': student.number,
            'student_group': student_group.name,
            'teachers': teacher_str,
            'actual_date': get_date_time_loc(actual_date),
            'student_tabs': student_tabs_html_string
        }
    )
    file_name = instances.get_student_path() + student.name + " index"
    asci_file_name = file_name.translate(translation_table)
    # print("BB21 - Write portfolio for", student.name)
    with open(asci_file_name + ".html", mode='w', encoding="utf-8") as file_portfolio:
        file_portfolio.write(student_index_html_string)
    return

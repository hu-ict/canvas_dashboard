from lib.build_plotly_hover import get_hover_rubrics_comments, get_hover_comments, get_hover_assignment, \
    get_hover_grade, get_hover_status
from lib.file import read_plotly
from lib.lib_date import get_date_time_loc
from lib.translation_table import translation_table
from model.perspective.Status import NOT_YET_GRADED, BEFORE_DEADLINE, GRADED, MISSED_ITEM


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
    for grade_moment in course.grade_moments.moments:
        tabs[grade_moment.replace(" ", "_").lower()] = grade_moment
    tabs_html_string = ""
    tab_count = 0
    for tab in tabs:
        if tab_count == 0:
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
        tab_count += 1
    tab_count = 0
    for tab in tabs:
        if tab_count == 0:
            tabs_html_string += '<div class="student_view ' + tab + '">\n'
        else:
            tabs_html_string += '<div style="display: None" class="student_view '+tab+'">\n'
        tabs_html_string += student_tabs[tab]
        tabs_html_string += '</div>\n'
        tab_count += 1
    return tabs_html_string


def build_level_moments(course_id, course, moment, moment_submissions, templates, levels):
    assignments = course.get_level_moments_by_query(moment)

    # print("BLM02 - len(level_moment_submissions)",len(level_moment_submissions), "for level_moment", level_moment)
    if len(moment_submissions) == 0:
        progress_label = levels.level_series[course.level_moments.levels].get_status(BEFORE_DEADLINE).label
        progress_color = levels.level_series[course.level_moments.levels].get_status(BEFORE_DEADLINE).color
        comments = "Leeg"
        level_moment_html_string = templates['level_moment'].substitute(
            {'level_moment_title': moment,
             'url':  "",
             'progress_label': progress_label,
             'progress_color': progress_color,
             'submitted_date': "Leeg",
             'grader_name': "leeg",
             'graded_date': "Leeg",
             'comments': comments,
             'reflection': "<p>Geen reflectie van student</p>"
             }
        )
    else:
        level_moment_html_string = ""
        for moment_submission in moment_submissions:
            # print("BLM04 -", level_moment_submission.assignment_name)
            comments = get_comments(moment_submission.comments)
            url = "https://canvas.hu.nl/courses/" + str(course_id) + "/gradebook/speed_grader?assignment_id=" + str(
                moment_submission.assignment_id) + "&student_id=" + str(moment_submission.student_id)
            if moment_submission.graded:
                progress_label = levels.level_series[course.level_moments.levels].grades[str(int(moment_submission.score))].label
                progress_color = levels.level_series[course.level_moments.levels].grades[str(int(moment_submission.score))].color
            else:
                # Niet bepaald
                progress_label = levels.level_series[course.level_moments.levels].get_status(NOT_YET_GRADED).label
                progress_color = levels.level_series[course.level_moments.levels].get_status(NOT_YET_GRADED).color
            if moment_submission.body == "":
                moment_submission.body = "Geen reflectie ingeleverd."
            reflection_html_string = templates['reflection'].substitute(
                {'submitted_date': get_date_time_loc(moment_submission.submitted_date),
                 'body': moment_submission.body
                 }
            )
            level_moment_html_string += templates['level_moment'].substitute(
                {'level_moment_title': moment_submission.assignment_name,
                 'url': url,
                 'progress_color': progress_color,
                 'progress_label': progress_label,
                 'submitted_date': get_date_time_loc(moment_submission.submitted_date),
                 'grader_name': moment_submission.grader_name,
                 'graded_date': get_date_time_loc(moment_submission.graded_date),
                 'comments': comments,
                 'reflection': reflection_html_string
                 }
            )

        # print("BLM09 -", student_tabs_html_string)
    return level_moment_html_string

# def get_badge_status(graded, score, points, level_series):
#     if graded:
#         if score == 0:  # "Niet zichtbaar"
#             # status = level_series.level_series["bin2"].levels["0"].label
#             cell_status = "status_missed"
#         elif score == points:
#             # portfolio items moet compleet zijn
#             # status = level_series.level_series["bin2"].levels["2"].label
#             cell_status = "status_complete"
#         else:  # Niet voldaan
#             # status = level_series.level_series["bin2"].levels["1"].label
#             cell_status = "status_incomplete"
#     else:  # Nog niet beoordeeld
#         # status = level_series.level_series["bin2"].levels["-2"].label
#         cell_status = "status_pending"
#     return cell_status


def build_bootstrap_portfolio(instances, course_id, course, student, actual_date, actual_day, templates, level_serie_collection):
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
        level_serie = level_serie_collection.level_series[course.perspectives[perspective.name].levels]
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
                if submission_sequence is None:
                    status_label = level_serie.get_status(BEFORE_DEADLINE).label
                    cell_status = "status_comming"
                else:
                    if submission_sequence.get_status() is GRADED:
                        cell_status = submission_sequence.get_complete_status()
                        if cell_status == "status_incomplete":
                            status_label = level_serie.grades["1"].label
                        else:
                            status_label = level_serie.grades["2"].label
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_summary[learning_outcome_id]['total_points'] += submission_sequence.get_score()
                    else:
                        if submission_sequence.get_status() is MISSED_ITEM:
                            cell_status = "status_missed"
                        else:
                            cell_status = "status_pending"
                        status_label = level_serie.get_status(submission_sequence.get_status()).label

                for learning_outcome_id in assignment_sequence.learning_outcomes:
                    if cell_status in learning_outcome_summary[learning_outcome_id]:
                        learning_outcome_summary[learning_outcome_id][cell_status] += 1

                badges = ""
                modal_content_html_string = ""
                portfolio_items_modal_html_string = ""
                if submission_sequence is not None:
                    teller = 0
                    for submission in submission_sequence.submissions:
                        # bouw de teksten voor het modal scherm
                        modal_content_html_string += "<p>"
                        level = level_serie_collection.level_series["bin2"].get_level_by_fraction(submission.score / submission_sequence.points)
                        modal_content_html_string += get_hover_assignment(True, submission)
                        if submission.graded:
                            modal_content_html_string += get_hover_grade(course, submission, level_serie.grades, level)
                        else:
                            modal_content_html_string += get_hover_status(submission, level_serie)
                        modal_content_html_string += get_comments(submission.comments)
                        modal_content_html_string += get_hover_rubrics_comments(course, submission, level_serie.grades)
                        modal_content_html_string += "</p>"
                    portfolio_items_modal_html_string = '<a class="badge mr-1" data-toggle="modal" data-target="#' + assignment_sequence.tag + '">Open</a>'
                    portfolio_items_modal_html_string += templates['portfolio_item_modal'].substitute(
                        {"portfolio_item_id": assignment_sequence.tag,
                         "portfolio_item": portfolio_item,
                         "content": modal_content_html_string})
                    for submission in submission_sequence.submissions:
                        if submission.status == GRADED:
                            if submission.score == submission.points:
                                badge_status = "status_complete"
                            else:
                                badge_status = "status_incomplete"
                        else:
                            if submission.status is MISSED_ITEM:
                                badge_status = "status_missed"
                            else:
                                badge_status = "status_pending"
                        teller += 1
                        url = "https://canvas.hu.nl/courses/" + str(
                            course_id) + "/gradebook/speed_grader?assignment_id=" + str(
                            submission.assignment_id) + "&student_id=" + str(student.id)
                        badges += '<a class="badge mr-1 '+badge_status+'" target="_blank" href="'+url+'">'+str(teller)+'</a>'
                date, day = assignment_sequence.get_date_day(submission_sequence, actual_day)
                if day < actual_day:
                    highlight = "danger"
                else:
                    highlight = "success"
                item_dict = {
                    "portfolio_item": portfolio_item,
                    "portfolio_item_id": assignment_sequence.tag,
                    "portfolio_item_modal": portfolio_items_modal_html_string,
                    "item_url": badges,
                    "portfolio_date": get_date_time_loc(date),
                    "portfolio_day": day,
                    "highlight": highlight,
                    "portfolio_status": status_label,
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
        portfolio_items_html_string += templates['portfolio_item'].substitute(portfolio_item)
    # portfolio_items_model_html_string = ""
    # for perspective in course.perspectives.values():
    #     for assignment_group_id in perspective.assignment_groups:
    #         assignment_groep = course.find_assignment_group(assignment_group_id)
    #         for assignment_sequence in assignment_groep.assignment_sequences:
    #             portfolio_items_model_html_string += templates['portfolio_item_modal'].substitute({"portfolio_item_id": assignment_sequence.tag, "portfolio_item": portfolio_item["portfolio_item"], "content": "Content"})

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
         'attendance_essential_count': str(int(student.student_attendance.essential_count)),
         'attendance_count': str(int(student.student_attendance.count)),
         'attendance_essential_percentage': str(int(student.student_attendance.essential_percentage*100)),
         'attendance_percentage': str(int(student.student_attendance.percentage*100)),
         'portfolio_items': portfolio_items_html_string,
         'portfolio_items_modal': "" #portfolio_items_modal_html_string
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


def build_bootstrap_student_index(instances, course_id, course, student, actual_date, actual_day, templates, levels):
    student_group = course.find_student_group(student.group_id)
    teacher_str = ""
    for teacher in student_group.teachers:
        teacher = course.find_teacher(teacher)
        teacher_str += teacher.name + ", "
    # progress_file_name = ".//" + student.name.replace(" ", "%20") + "%20progress.html"
    # progress_asci_file_name = progress_file_name.translate(translation_table)
    # # print("BB91 - Index", progress_file_name, portfolio_asci_file_name)
    student_group = course.find_student_group(student.group_id)
    student_tabs = {}
    for moment in course.level_moments.moments:
        level_moment_submissions = student.get_level_moment_submissions_by_query(moment)
        student_tabs[moment.replace(" ", "_").lower()] = build_level_moments(course_id, course, moment, level_moment_submissions, templates, levels)
    for moment in course.grade_moments.moments:
        grade_moment_submissions = student.get_grade_moment_submissions_by_query(moment)
        student_tabs[moment.replace(" ", "_").lower()] = build_level_moments(course_id, course, moment, grade_moment_submissions, templates, levels)

    if instances.is_instance_of("prop_courses"):
        student_tabs['portfolio'] = build_bootstrap_portfolio(instances, course_id, course, student, actual_date, actual_day, templates, levels)

    file_name = instances.get_student_path() + student.name + " progress.html"
    asci_file_name = file_name.translate(translation_table)
    student_tabs['voortgang'] = '<h2 class="mt-2">Voortgang</h2>'+read_plotly(asci_file_name)
    # print("BSI10 - ", student_tabs.keys())
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

from scripts.lib.build_plotly_hover import get_hover_assignment, \
    get_hover_grade, get_hover_status
from scripts.lib.file import read_plotly
from scripts.lib.lib_date import get_date_time_loc
from scripts.lib.lib_portfolio import TOTAL_POINTS, STATUS_COMPLETE, STATUS_INCOMPLETE, STATUS_MISSED, STATUS_PENDING, \
    STATUS_COMING
from scripts.model.perspective.Status import NOT_YET_GRADED, BEFORE_DEADLINE, GRADED, MISSED_ITEM

def get_submission_badges(assignment_sequence, submission_sequence, actual_day):
    # *******************************
    # Maak de submission_badges aan
    # *******************************
    badges = []
    teller = 0
    for assignment in assignment_sequence.assignments:
        if submission_sequence:
            submission = submission_sequence.get_submission_by_assignment(assignment.id)
            if submission:
                teller += 1
                badge = {}
                badge["status"] = submission.get_complete_status_css()
                badge["assignment_id"] = assignment.id
                badge["teller"] = teller
                badges.append(badge)
            else:
                if actual_day > assignment.day:
                    teller += 1
                    badge = {}
                    badge["status"] = STATUS_MISSED
                    badge["assignment_id"] = assignment.id
                    badge["teller"] = teller
                    badges.append(badge)
        else:
            if actual_day > assignment.day:
                teller += 1
                badge = {}
                badge["status"] = STATUS_MISSED
                badge["assignment_id"] = assignment.id
                badge["teller"] = teller
                badges.append(badge)
    return badges

def get_comments_html(comments):
    comments_html_string = ""
    if len(comments) > 0:
        for comment in comments:
            comments_html_string += get_date_time_loc(
                comment.date) + " " + comment.author_name + " - <i>" + comment.comment + "</i><br>"
    return comments_html_string


def get_feedback_list_html(course, student_id, feedback_list, templates, feedback_colors):
    feedback_list_html_string = ""
    for feedback in feedback_list:
        url = "https://canvas.hu.nl/courses/" + str(course.canvas_id) + "/gradebook/speed_grader?assignment_id=" \
              + str(feedback.assignment_id) + "&student_id=" + str(student_id)
        background_color = feedback_colors[feedback.positive_neutral_negative]["color"]
        feedback_list_html_string += templates['feedback'].substitute({
            "feedback_color": background_color,
            "date": get_date_time_loc(feedback.date),
            "author_name": feedback.author_name,
            "comment": feedback.comment,
            "url": url,
            "assignment_name": feedback.assignment_name,
            "grade": feedback.grade
        })
    return feedback_list_html_string


def get_rubrics_comments(course, submission, grade):
    if len(submission.rubrics) == 0:
        return ""
    l_hover = "<br><b>Criteria:</b>"
    for criterion_score in submission.rubrics:
        # print("BP10 -", submission.assignment_id, criterion_score)
        assignment = course.find_assignment(submission.assignment.id)
        # print("BP11 -", assignment)
        assignment_criterion = assignment.get_criterion(criterion_score.id)
        if assignment_criterion is None:
            continue
        # if submission.assignment_id ==  298261 and submission.student_id == 148369:
        # print("BP11 -", assignment_criterion, criterion_score)
        if criterion_score.rating_id:
            if assignment_criterion.get_rating(criterion_score.rating_id) is not None:
                l_hover += "<br>- " + assignment_criterion.description + " <b>" + assignment_criterion.get_rating(
                    criterion_score.rating_id).description + "</b>"
            # if submission.assignment_id == 298261 and submission.student_id == 148369:
            #     print("BP14 -", l_hover)
        else:
            if criterion_score.score == 0:
                l_hover += "<br>- " + assignment_criterion.description + " <b>" + grade.label + "</b>"
                # if submission.assignment_id == 298261 and submission.student_id == 148369:
                #     print("BP15 -", l_hover)
            else:
                l_hover += "<br>- " + assignment_criterion.description + " <b>" + str(criterion_score.score) + "</b>"
                # if submission.assignment_id == 298261 and submission.student_id == 148369:
                #     print("BP16 -", l_hover)

        if criterion_score.comment:
            l_hover += "<br><i>" + criterion_score.comment + "</i>"
    return l_hover


def build_student_tabs(instance, course, student_tab_content, student_tabs):
    for assignment in course.get_level_moments():
        student_tabs[assignment.name.replace(" ", "_").lower()] = assignment.name
    for assignment in course.get_grade_moments():
        student_tabs[assignment.name.replace(" ", "_").lower()] = assignment.name
    tabs_html_string = ""
    tab_count = 0
    for tab in student_tabs:
        if tab_count == 0:
            tabs_html_string += '<div class="student_view ' + tab + '"><ul class="nav nav-tabs">\n'
        else:
            tabs_html_string += '<div style="display: None" class="student_view ' + tab + '"><ul class="nav nav-tabs">\n'
        for tab_inner in student_tabs:
            if tab == tab_inner:
                active = "active"
                page = "page"
            else:
                active = ""
                page = "false"
            inner_tab = "'" + tab_inner + "'"
            tabs_html_string += '<li class="nav-item"><a onclick="setStudentView(' + inner_tab + ')" class="nav-link ' + active + '" aria-current="' + page + '" href="#">' + \
                                student_tabs[tab_inner] + '</a></li>\n'
        tabs_html_string += '</ul></div>'
        tab_count += 1
    tab_count = 0
    # print("BBS31 -", student_tabs)
    # print("BBS32 -", student_tab_content.keys())
    for tab in student_tabs:
        if tab_count == 0:
            tabs_html_string += '<div class="student_view ' + tab + '">\n'
        else:
            tabs_html_string += '<div style="display: None" class="student_view ' + tab + '">\n'
        tabs_html_string += student_tab_content[tab]
        tabs_html_string += '</div>\n'
        tab_count += 1
    return tabs_html_string


def build_moment(course_id, course, level_serie, assignment_name, submission, templates):
    # print("BLM02 - len(moment_submissions)", len(moment_submissions), "for level_moment", moment)
    if submission is None:
        # print("BLM03 - len(moment_submissions) == 0")
        progress_label = level_serie.get_status(BEFORE_DEADLINE).label
        progress_color = level_serie.get_status(BEFORE_DEADLINE).color
        comments = "Leeg"
        url = "https://canvas.hu.nl/courses/" + str(course_id)
        learning_outcomes_table = ""
        level_moment_html_string = templates['level_moment'].substitute(
            {'level_moment_title': assignment_name,
             'url': url,
             'progress_label': progress_label,
             'progress_color': progress_color,
             'submitted_date': "leeg",
             'grader_name': "leeg",
             'graded_date': "leeg",
             'comments': comments,
             'learning_outcomes_table': learning_outcomes_table,
             'reflection': ""
             }
        )
    else:
        level_moment_html_string = ""

        # print("BLM04 -", moment_submission.assignment_name, moment_submission.graded, moment_submission.grade)
        # print("BLM05 -", level_serie)
        comments = get_comments_html(submission.comments)
        url = "https://canvas.hu.nl/courses/" + str(course_id) + "/gradebook/speed_grader?assignment_id=" + str(
            submission.assignment.id) + "&student_id=" + str(submission.student_id)
        if submission.graded:
            if submission.grade is not None:
                progress_label = level_serie.grades[submission.grade].label
                progress_color = level_serie.grades[submission.grade].color
            else:
                progress_label = level_serie.grades["0"].label
                progress_color = level_serie.grades["0"].color
        else:
            # Niet bepaald
            progress_label = level_serie.get_status(NOT_YET_GRADED).label
            progress_color = level_serie.get_status(NOT_YET_GRADED).color
        assignment = course.find_assignment(submission.assignment.id)
        if "online_text_entry" in assignment.submission_types:
            if submission.body is None or submission.body == "":
                submission.body = "Geen reflectie ingeleverd."
            reflection_html_string = templates['reflection'].substitute(
                {'submitted_date': get_date_time_loc(submission.submitted_date),
                 'body': submission.body
                 }
            )
        else:
            reflection_html_string = ""
        learning_outcome_list = ""
        for rubric in assignment.rubrics:
            criterium = submission.get_criterium_score(rubric.id)
            if criterium:
                l_score = str(int(criterium.score))
                l_comment = criterium.comment
            else:
                l_score = "-1"
                l_comment = ""

            l_label = level_serie.grades[l_score].label
            l_color = level_serie.grades[l_score].color
            learning_outcome_list += templates['learning_outcome_row'].substitute(
                {'learning_outcome': rubric.description,
                 'color': l_color,
                 'label': l_label,
                 'argumentatie': l_comment})
        learning_outcomes_table = templates['learning_outcomes_table'].substitute(
            {'learning_outcome_list': learning_outcome_list})
        level_moment_html_string += templates['level_moment'].substitute(
            {'level_moment_title': submission.assignment.name,
             'url': url,
             'progress_color': progress_color,
             'progress_label': progress_label,
             'submitted_date': get_date_time_loc(submission.submitted_date),
             'grader_name': submission.grader_name,
             'graded_date': get_date_time_loc(submission.graded_date),
             'learning_outcomes_table': learning_outcomes_table,
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


def build_bootstrap_portfolio(course_instance, course_id, course, student, student_results, actual_date, actual_day, templates,
                              level_serie_collection):
    portfolio_items_html_string = ""
    portfolio_items = []
    learning_outcome_totals = {}
    for learning_outcome in course.learning_outcomes:
        learning_outcome_totals[learning_outcome.id] = {
            TOTAL_POINTS: 0,
            STATUS_COMPLETE: 0,
            STATUS_INCOMPLETE: 0,
            STATUS_MISSED: 0,
            STATUS_PENDING: 0
        }
    for perspective in course.perspectives.values():
        # print("BBS51 -", )
        for assignment_group_id in perspective.assignment_group_ids:
            assignment_groep = course.get_assignment_group(assignment_group_id)
            level_serie = level_serie_collection.level_series[assignment_groep.levels]
            for assignment_sequence in assignment_groep.assignment_sequences:
                # ********************************
                # Start portfolio item in matrix
                # ********************************
                portfolio_item_name = assignment_sequence.name + " (" + str(len(assignment_sequence.assignments)) + ")"
                submission_sequence = student_results.get_submission_sequence_by_name(assignment_sequence.name)
                if submission_sequence is None:
                    # No submissions
                    portfolio_item_date, portfolio_item_day = assignment_sequence.get_date_day(submission_sequence, actual_day)
                    if actual_day <= portfolio_item_day:
                        status_label = level_serie.get_status(BEFORE_DEADLINE).label
                        cell_status = STATUS_COMING
                    else:
                        status_label = level_serie.get_status(MISSED_ITEM).label
                        cell_status = STATUS_MISSED
                else:
                    cell_status = submission_sequence.get_complete_status_css()
                    if submission_sequence.get_status() is GRADED:
                        if cell_status == STATUS_INCOMPLETE:
                            status_label = level_serie.grades["0"].label
                        else:
                            status_label = level_serie.grades["2"].label
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_totals[learning_outcome_id][TOTAL_POINTS] += submission_sequence.get_score()
                    else:
                        status_label = level_serie.get_status(submission_sequence.get_status()).label

                for learning_outcome_id in assignment_sequence.learning_outcomes:
                    if cell_status in learning_outcome_totals[learning_outcome_id]:
                        learning_outcome_totals[learning_outcome_id][cell_status] += 1

                badges = get_submission_badges(assignment_sequence, submission_sequence, actual_day)
                submission_badges = ""
                for badge in badges:
                    url = "https://canvas.hu.nl/courses/" + str(
                        course_id) + "/gradebook/speed_grader?assignment_id=" + str(badge["assignment_id"]) + "&student_id=" + str(student.id)
                    submission_badges += '<a class="badge mr-1 ' + badge["status"] + '" target="_blank" href="' + url + '">' + str(
                        badge["teller"]) + '</a>'

                modal_content_html_string = ""
                # **********************************
                # Bouw het modal window met feedback
                # **********************************
                portfolio_items_modal_html_string = ""
                if submission_sequence is not None:
                    for submission in submission_sequence.submissions:
                        # bouw de teksten voor het modal scherm
                        modal_content_html_string += "<p>"
                        modal_content_html_string += get_hover_assignment(True, submission)
                        if submission.graded:
                            grade = level_serie.grades[submission.grade]
                            modal_content_html_string += get_hover_grade(course, submission, grade)
                            modal_content_html_string += get_rubrics_comments(course, submission, grade)
                        else:
                            status = level_serie.status[submission.status]
                            modal_content_html_string += get_hover_status(submission, status)
                        modal_content_html_string += get_comments_html(submission.comments)
                        modal_content_html_string += "</p>"
                    portfolio_items_modal_html_string += templates['portfolio_item_modal'].substitute(
                        {"portfolio_item_id": assignment_sequence.tag,
                         "portfolio_item": portfolio_item_name,
                         "content": modal_content_html_string})
                    portfolio_items_modal_html_string += '<a class="badge btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#target' + assignment_sequence.tag + '"' + " onclick='scrollToTop()'>Detail</a>"
                date, day = assignment_sequence.get_date_day(submission_sequence, actual_day)
                if day < actual_day:
                    background_color = "#ffb3b3"
                else:
                    background_color = "#c6ecd9"
                portfolio_item_dict = {
                    "portfolio_item": portfolio_item_name,
                    "portfolio_item_id": assignment_sequence.tag,
                    "portfolio_item_modal": portfolio_items_modal_html_string,
                    "submission_badges": submission_badges,
                    "portfolio_date": get_date_time_loc(date),
                    "portfolio_day": day,
                    "background_color": background_color,
                    "portfolio_status": status_label,
                    "cell_status": cell_status
                }
                learning_outcomes_row_html_string = ""
                for learning_outcome in course.learning_outcomes:
                    if learning_outcome.id in assignment_sequence.learning_outcomes:
                        learning_outcomes_row_html_string += '<td style="text-align:center;"><span class="badge badge-primary">' + str(
                            assignment_sequence.points) + '</span></td>'
                    else:
                        learning_outcomes_row_html_string += '<td></td>'
                portfolio_item_dict["learning_outcomes"] = learning_outcomes_row_html_string
                portfolio_items.append(portfolio_item_dict)
    portfolio_items = sorted(portfolio_items, key=lambda p: p['portfolio_day'])

    #**************************
    # Opbouwen tabel met totals
    #**************************
    learning_outcomes_header_html_string = ""
    total_points_html = ""
    complete_items_html = ""
    incomplete_items_html = ""
    status_missed_items_html = ""
    status_pending_items_html = ""
    for learning_outcome in course.learning_outcomes:
        items = learning_outcome_totals[learning_outcome.id][STATUS_COMPLETE]
        score = learning_outcome_totals[learning_outcome.id][TOTAL_POINTS]
        grade = learning_outcome.get_grade(items, score)
        background_color = level_serie_collection.level_series["grade"].grades[grade].color
        learning_outcomes_header_html_string += '<th scope = "col" style="text-align: center; color:white; background-color:''' + background_color + '''">''' + learning_outcome.id + '</th>'
        # behaalde_punten_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['total_points'])+"</td>"
        # print("BBP51 -", items, score, grade, background_color)
        complete_items_html += "<td>" + str(
            learning_outcome_totals[learning_outcome.id][STATUS_COMPLETE]) + " (" + str(
            learning_outcome_totals[learning_outcome.id][TOTAL_POINTS]) + ")</td>"
        incomplete_items_html += "<td>" + str(
            learning_outcome_totals[learning_outcome.id][STATUS_INCOMPLETE]) + "</td>"
        status_missed_items_html += "<td>" + str(learning_outcome_totals[learning_outcome.id]['status_missed']) + "</td>"
        status_pending_items_html += "<td>" + str(learning_outcome_totals[learning_outcome.id]['status_pending']) + "</td>"
    portfolio_summary_html = templates['portfolio_summary'].substitute({
        'learning_outcomes': learning_outcomes_header_html_string,
        'status_complete_items': complete_items_html,
        'status_incomplete_items': incomplete_items_html,
        'status_missed_items': status_missed_items_html,
        'status_pending_items': status_pending_items_html,
    })

    # **************************
    # opbouwen portfolio-matrix
    # **************************
    for portfolio_item in portfolio_items:
        # print(portfolio_item)
        portfolio_items_html_string += templates['portfolio_item'].substitute(portfolio_item)
    # portfolio_items_model_html_string = ""
    # for perspective in course.perspectives.values():
    #     for assignment_group_id in perspective.assignment_groups:
    #         assignment_groep = course.find_assignment_group(assignment_group_id)
    #         for assignment_sequence in assignment_groep.assignment_sequences:
    #             portfolio_items_model_html_string += templates['portfolio_item_modal'].substitute({"portfolio_item_id": assignment_sequence.tag, "portfolio_item": portfolio_item["portfolio_item"], "content": "Content"})
    attendance_html = ""
    if course_instance.course_code in ["TICT-V1S1-24"]:
        attendance_dict = {}
        attendance_dict['attendance_essential_count'] = str(int(student_results.student_attendance.essential_count))
        attendance_dict['attendance_count'] = str(int(student_results.student_attendance.count))
        attendance_dict['attendance_essential_percentage'] = str(
            int(student_results.student_attendance.essential_percentage * 100))
        attendance_dict['attendance_percentage'] = str(int(student_results.student_attendance.percentage * 100))
        attendance_html = templates['attendance'].substitute(attendance_dict)

    groups_1_group = course.find_groups_1_group(student.groups_1_group_id)
    if groups_1_group is not None:
        groups_1_group_name = groups_1_group.name
    else:
        groups_1_group_name = "leeg"

    portfolio_matrix_html = templates['portfolio_matrix'].substitute({
        'learning_outcomes': learning_outcomes_header_html_string,
        'portfolio_items': portfolio_items_html_string
    })

    portfolio_dict = {
        'portfolio_summary': portfolio_summary_html,
        'attendance': attendance_html,
        'portfolio_matrix': portfolio_matrix_html,
        'portfolio_items_modal': ""  # portfolio_items_modal_html_string
    }
    portfolio_html_string = templates['portfolio'].substitute(portfolio_dict)
    return portfolio_html_string


def build_bootstrap_feedback(course, student_results, templates, feedback_colors):
    student_feedback_html_string = ""
    for learning_outcome in student_results.learning_outcomes:
        student_feedback_html_string += templates['learning_outcome_feedback'].substitute(
            {
                'learning_outcome_short': student_results.learning_outcomes[learning_outcome].short,
                'learning_outcome_id': student_results.learning_outcomes[learning_outcome].id,
                'feedback_rows': get_feedback_list_html(course, student_results.id, student_results.learning_outcomes[learning_outcome].feedback_list, templates, feedback_colors)
            })
    student_feedback_html_string += templates['learning_outcome_feedback'].substitute(
        {
            'learning_outcome_short': "Algemene feedback",
            'learning_outcome_id': "AF",
            'feedback_rows': get_feedback_list_html(course, student_results.id, student_results.general_feedback_list, templates, feedback_colors)
        })

    # for perspective in student_results.perspectives.values():
    #     l_level_serie = level_serie_collection.level_series[course.perspectives[perspective.name].levels]
    #     for submission_sequence in perspective.submission_sequences:
    #         for submission in submission_sequence.submissions:
    #             if submission.grade:
    #                 grade = l_level_serie.grades[submission.grade]
    #                 student_feedback_html_string += templates['submission_feedback'].substitute(
    #                     {
    #                         'assignment_name': submission.assignment_name,
    #                         'grade': grade.label,
    #                         'comments': get_comments_html(submission.comments),
    #                         'rubrics': get_rubrics_comments(course, submission, grade)
    #                     })

    return student_feedback_html_string


def build_bootstrap_student_index(course_instance, course_id, course, student_results, actual_date, actual_day, templates,
                                  dashboard):
    student = course.find_student(student_results.id)

    # ******************************
    # Student top of page header
    # ******************************
    groups_1_group = course.find_groups_1_group(student.groups_1_group_id)
    if groups_1_group is not None:
        groups_1_group_name = groups_1_group.name
    else:
        groups_1_group_name = "leeg"
    groups_2_group_name = ""
    groups_2_group = course.find_groups_2_group(student.groups_2_group_id)
    if groups_2_group is not None:
        groups_2_group_name = groups_2_group.name

    groups_1_group_teacher_str = ""
    groups_2_group_teacher_str = ""
    for assessor in student.assessors:
        # print("BBS41 -", assessor.teacher_id, assessor)
        if assessor.student_group_collection == "groups_1":
            groups_1_group_teacher_str += "<li>"+course.find_teacher(assessor.teacher_id).name+" voor "+course.get_assignment_group(assessor.assignment_group_id).name+"</li>"
        if assessor.student_group_collection == "groups_2":
            groups_2_group_teacher_str += "<li>"+course.find_teacher(assessor.teacher_id).name+" voor "+course.get_assignment_group(assessor.assignment_group_id).name+"</li>"

    # ******************************
    # Student index menu
    # ******************************
    student_tab_content = {}
    for level_moment in course.get_level_moments():
        submission = student_results.student_level_moments.get_submission_by_assignment(level_moment.id)
        # print("BBS31 -", moment, len(level_moment_submissions))
        level_serie = dashboard.level_serie_collection.level_series[course.level_moments.levels]
        student_tab_content[level_moment.name.replace(" ", "_").lower()] = build_moment(course_id, course, level_serie,
                                                                              level_moment.name, submission, templates)
    for grade_moment in course.get_grade_moments():
        submission = student_results.student_grade_moments.get_submission_by_assignment(grade_moment.id)
        level_serie = dashboard.level_serie_collection.level_series[course.grade_moments.levels]
        # print("BBSI04 -", moment, len(grade_moment_submissions))
        student_tab_content[grade_moment.name.replace(" ", "_").lower()] = build_moment(course_id, course, level_serie,
                                                                              grade_moment.name, submission, templates)
    # print("BBSI02 -", student_tabs)
    if 'voortgang' in dashboard.student_tabs:
        # Importeren plotly html in index html file
        student_name = student.email.split("@")[0].lower()
        file_name_html = course_instance.get_temp_path() + student_name + "_progress.html"
        student_tab_content['voortgang'] = '<h2 class="mt-2">Voortgang</h2>' + read_plotly(file_name_html)
    if 'portfolio' in dashboard.student_tabs:
        student_tab_content['portfolio'] = build_bootstrap_portfolio(course_instance, course_id, course, student,
                                                                     student_results, actual_date, actual_day,
                                                                     templates, dashboard.level_serie_collection)
    if 'feedback' in dashboard.student_tabs:
        student_tab_content['feedback'] = build_bootstrap_feedback(course, student_results, templates,
                                                                   dashboard.feedback_colors)

    # print("BSI10 - ", student_tabs.keys())
    student_tabs_html_string = build_student_tabs(course_instance, course, student_tab_content,
                                                  dashboard.student_tabs)
    student_index_html_string = templates['student_index'].substitute(
        {
            'semester': course.name,
            'student_name': student.name,
            'student_email': student.email,
            'student_number': student.number,
            'groups_1_label': dashboard.dashboard_tabs["groups_1"],
            'groups_1_name': groups_1_group_name,
            'groups_1_teachers': groups_1_group_teacher_str,
            'groups_2_label': dashboard.dashboard_tabs["groups_2"],
            'groups_2_name': groups_2_group_name,
            'groups_2_teachers': groups_2_group_teacher_str,
            'actual_date': get_date_time_loc(actual_date),
            'student_tabs': student_tabs_html_string
        }
    )
    student_name = student.email.split("@")[0].lower()
    file_name_html = course_instance.get_html_student_path() + student_name + "_index.html"
    # print("BB21 - Write portfolio for", student.name)
    with open(file_name_html, mode='w', encoding="utf-8") as file_portfolio:
        file_portfolio.write(student_index_html_string)
    return

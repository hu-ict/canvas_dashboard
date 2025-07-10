from lib.build_plotly_hover import get_hover_assignment, \
    get_hover_grade, get_hover_status
from lib.file import read_plotly
from lib.lib_date import get_date_time_loc
from model.perspective.Status import NOT_YET_GRADED, BEFORE_DEADLINE, GRADED, MISSED_ITEM


def get_comments_html(comments):
    comments_html_string = ""
    if len(comments) > 0:
        for comment in comments:
            comments_html_string += get_date_time_loc(
                comment.date) + " " + comment.author_name + " - <i>" + comment.comment + "</i><br>"
    return comments_html_string


def get_feedback_list_html(feedback_list, templates):
    feedback_list_html_string = ""
    for feedback in feedback_list:
        feedback_list_html_string += templates['feedback'].substitute({
            "date": get_date_time_loc(feedback.date),
            "author_name": feedback.author_name,
            "author_id": feedback.author_id,
            "comment": feedback.comment,
            "url": "",
            "assignment_name": feedback.assignment_name,
            "submission_id": feedback.submission_id,
            "grade": feedback.grade
        })
    return feedback_list_html_string


def get_rubrics_comments(course, submission, grade):
    if len(submission.rubrics) == 0:
        return ""
    l_hover = "<br><b>Criteria:</b>"
    for criterion_score in submission.rubrics:
        # print("BP10 -", submission.assignment_id, criterion_score)
        assignment = course.find_assignment(submission.assignment_id)
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
    for level_moment in course.level_moments.moments:
        student_tabs[level_moment.replace(" ", "_").lower()] = level_moment
    for grade_moment in course.grade_moments.moments:
        student_tabs[grade_moment.replace(" ", "_").lower()] = grade_moment
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
    for tab in student_tabs:
        if tab_count == 0:
            tabs_html_string += '<div class="student_view ' + tab + '">\n'
        else:
            tabs_html_string += '<div style="display: None" class="student_view ' + tab + '">\n'
        tabs_html_string += student_tab_content[tab]
        tabs_html_string += '</div>\n'
        tab_count += 1
    return tabs_html_string


def build_moments(course_id, course, moment, level_serie, moment_submissions, templates):
    # print("BLM02 - len(moment_submissions)", len(moment_submissions), "for level_moment", moment)
    if len(moment_submissions) == 0:
        # print("BLM03 - len(moment_submissions) == 0")
        progress_label = level_serie.get_status(BEFORE_DEADLINE).label
        progress_color = level_serie.get_status(BEFORE_DEADLINE).color
        comments = "Leeg"
        url = "https://canvas.hu.nl/courses/" + str(course_id)
        learning_outcomes_table = ""
        level_moment_html_string = templates['level_moment'].substitute(
            {'level_moment_title': moment,
             'url': url,
             'progress_label': progress_label,
             'progress_color': progress_color,
             'submitted_date': "Leeg",
             'grader_name': "leeg",
             'graded_date': "Leeg",
             'comments': comments,
             'learning_outcomes_table': learning_outcomes_table,
             'reflection': ""
             }
        )
    else:
        level_moment_html_string = ""
        for moment_submission in moment_submissions:
            # print("BLM04 -", moment_submission.assignment_name, moment_submission.graded, moment_submission.grade)
            # print("BLM05 -", level_serie)
            comments = get_comments_html(moment_submission.comments)
            url = "https://canvas.hu.nl/courses/" + str(course_id) + "/gradebook/speed_grader?assignment_id=" + str(
                moment_submission.assignment_id) + "&student_id=" + str(moment_submission.student_id)
            if moment_submission.graded:
                if moment_submission.grade is not None:
                    progress_label = level_serie.grades[moment_submission.grade].label
                    progress_color = level_serie.grades[moment_submission.grade].color
                else:
                    progress_label = level_serie.grades["0"].label
                    progress_color = level_serie.grades["0"].color
            else:
                # Niet bepaald
                progress_label = level_serie.get_status(NOT_YET_GRADED).label
                progress_color = level_serie.get_status(NOT_YET_GRADED).color
            assignment = course.find_assignment(moment_submission.assignment_id)
            if "online_text_entry" in assignment.submission_types:
                if moment_submission.body is None or moment_submission.body == "":
                    moment_submission.body = "Geen reflectie ingeleverd."
                reflection_html_string = templates['reflection'].substitute(
                    {'submitted_date': get_date_time_loc(moment_submission.submitted_date),
                     'body': moment_submission.body
                     }
                )
            else:
                reflection_html_string = ""
            learning_outcome_list = ""
            for rubric in assignment.rubrics:
                criterium = moment_submission.get_criterium_score(rubric.id)
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
                {'level_moment_title': moment_submission.assignment_name,
                 'url': url,
                 'progress_color': progress_color,
                 'progress_label': progress_label,
                 'submitted_date': get_date_time_loc(moment_submission.submitted_date),
                 'grader_name': moment_submission.grader_name,
                 'graded_date': get_date_time_loc(moment_submission.graded_date),
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


def build_bootstrap_portfolio(instance, course_id, course, student, student_results, actual_date, actual_day, templates,
                              level_serie_collection):
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
                submission_sequence = student_results.get_submission_sequence_by_name(assignment_sequence.name)
                student_group = course.find_project_group(student.project_id)
                teacher_str = ""
                if student_group is not None:
                    for teacher in student_group.teachers:
                        teacher = course.find_teacher(teacher)
                        teacher_str += teacher.name + ", "
                if submission_sequence is None:
                    status_label = level_serie.get_status(BEFORE_DEADLINE).label
                    cell_status = "status_comming"
                else:
                    cell_status = submission_sequence.get_complete_status_css()
                    if submission_sequence.get_status() is GRADED:
                        if cell_status == "status_incomplete":
                            status_label = level_serie.grades["0"].label
                        else:
                            status_label = level_serie.grades["2"].label
                            for learning_outcome_id in assignment_sequence.learning_outcomes:
                                learning_outcome_summary[learning_outcome_id][
                                    'total_points'] += submission_sequence.get_score()
                    else:
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
                         "portfolio_item": portfolio_item,
                         "content": modal_content_html_string})
                    portfolio_items_modal_html_string += '<a class="badge btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#target' + assignment_sequence.tag + '"' + " onclick='scrollToTop()'>Detail</a>"
                    for submission in submission_sequence.submissions:
                        badge_status = submission.get_complete_status_css()
                        teller += 1
                        url = "https://canvas.hu.nl/courses/" + str(
                            course_id) + "/gradebook/speed_grader?assignment_id=" + str(
                            submission.assignment_id) + "&student_id=" + str(student.id)
                        badges += '<a class="badge mr-1 ' + badge_status + '" target="_blank" href="' + url + '">' + str(
                            teller) + '</a>'
                date, day = assignment_sequence.get_date_day(submission_sequence, actual_day)
                if day < actual_day:
                    background_color = "#ffb3b3"
                else:
                    background_color = "#c6ecd9"
                item_dict = {
                    "portfolio_item": portfolio_item,
                    "portfolio_item_id": assignment_sequence.tag,
                    "portfolio_item_modal": portfolio_items_modal_html_string,
                    "item_url": badges,
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
        items = learning_outcome_summary[learning_outcome.id]['status_complete']
        score = learning_outcome_summary[learning_outcome.id]['total_points']
        grade = learning_outcome.get_grade(items, score)
        background_color = level_serie_collection.level_series["grade"].grades[grade].color
        learning_outcomes_header_html_string += '<th scope = "col" style="text-align: center; color:white; background-color:''' + background_color + '''">''' + learning_outcome.id + '</th>'
        # behaalde_punten_html += "<td>"+str(learning_outcome_summary[learning_outcome.id]['total_points'])+"</td>"
        # print("BBP51 -", items, score, grade, background_color)
        complete_items_html += "<td>" + str(
            learning_outcome_summary[learning_outcome.id]['status_complete']) + " (" + str(
            learning_outcome_summary[learning_outcome.id]['total_points']) + ")</td>"
        incomplete_items_html += "<td>" + str(
            learning_outcome_summary[learning_outcome.id]['status_incomplete']) + "</td>"
        niet_gemaakt_html += "<td>" + str(learning_outcome_summary[learning_outcome.id]['status_missed']) + "</td>"
        niet_beoordeeld_html += "<td>" + str(learning_outcome_summary[learning_outcome.id]['status_pending']) + "</td>"

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
    if instance.is_instance_of("prop_courses"):
        attendance_dict = {}
        attendance_dict['attendance_essential_count'] = str(int(student_results.student_attendance.essential_count))
        attendance_dict['attendance_count'] = str(int(student_results.student_attendance.count))
        attendance_dict['attendance_essential_percentage'] = str(
            int(student_results.student_attendance.essential_percentage * 100))
        attendance_dict['attendance_percentage'] = str(int(student_results.student_attendance.percentage * 100))
        attendance_html = templates['attendance'].substitute(attendance_dict)

    project_group = course.find_project_group(student.project_id)
    if project_group is not None:
        project_group_name = project_group.name
    else:
        project_group_name = "leeg"
    portfolio_dict = {'semester': course.name,
                      'student_name': student.name,
                      'student_email': student.email,
                      'student_number': student.number,
                      'student_group': project_group_name,
                      'teachers': teacher_str,
                      'actual_date': get_date_time_loc(actual_date),
                      'behaalde_punten': behaalde_punten_html,
                      'complete_items': complete_items_html,
                      'incomplete_items': incomplete_items_html,
                      'niet_gemaakt': niet_gemaakt_html,
                      'niet_beoordeeld': niet_beoordeeld_html,
                      'attendance': attendance_html,
                      'learning_outcomes': learning_outcomes_header_html_string,
                      'portfolio_items': portfolio_items_html_string,
                      'portfolio_items_modal': ""  # portfolio_items_modal_html_string
                      }

    portfolio_html_string = templates['portfolio'].substitute(portfolio_dict)

    return portfolio_html_string


def build_bootstrap_feedback(course, student_results, templates, level_serie_collection):
    student_feedback_html_string = templates['learning_outcome_feedback'].substitute(
        {
            'learning_outcome_short': "Algemene feedback",
            'learning_outcome_id': "AF",
            'feedback_rows': get_feedback_list_html(student_results.general_feedback_list, templates)
        })
    for learning_outcome in student_results.learning_outcomes:
        student_feedback_html_string += templates['learning_outcome_feedback'].substitute(
            {
                'learning_outcome_short': student_results.learning_outcomes[learning_outcome].short,
                'learning_outcome_id': student_results.learning_outcomes[learning_outcome].id,
                'feedback_rows': get_feedback_list_html(
                    student_results.learning_outcomes[learning_outcome].feedback_list, templates)
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


def build_bootstrap_student_index(instance, course_id, course, student_results, actual_date, actual_day, templates,
                                  dashboard):
    student = course.find_student(student_results.id)

    project_group_teacher_str = ""

    project_group = course.find_project_group(student.project_id)
    if project_group is not None:
        project_group_name = project_group.name
        i = 0
        for teacher in project_group.teachers:
            project_group_teacher_str += course.find_teacher(teacher).name
            if i < len(project_group.teachers) - 1:
                project_group_teacher_str += ", "
            i += 1
    else:
        project_group_name = "leeg"

    guild_group_teacher_str = ""
    guild_group_name = ""
    guild_group = course.find_guild_group(student.guild_id)
    if guild_group is not None:
        guild_group_name = guild_group.name
        i = 0
        for teacher in guild_group.teachers:
            guild_group_teacher_str += course.find_teacher(teacher).name
            if i < len(guild_group.teachers) - 1:
                guild_group_teacher_str += ", "
            i += 1

    student_tab_content = {}
    for moment in course.level_moments.moments:
        level_moment_submissions = student_results.get_level_moment_submissions_by_query([moment])
        # print("BBS31 -", moment, len(level_moment_submissions))
        level_serie = dashboard.level_serie_collection.level_series[course.level_moments.levels]
        student_tab_content[moment.replace(" ", "_").lower()] = build_moments(course_id, course, moment, level_serie,
                                                                              level_moment_submissions, templates)
    for moment in course.grade_moments.moments:
        grade_moment_submissions = student_results.get_grade_moment_submissions_by_query([moment])
        level_serie = dashboard.level_serie_collection.level_series[course.grade_moments.levels]
        # print("BBSI04 -", moment, len(grade_moment_submissions))
        student_tab_content[moment.replace(" ", "_").lower()] = build_moments(course_id, course, moment, level_serie,
                                                                              grade_moment_submissions, templates)

    # print("BBSI02 -", student_tabs)
    if 'voortgang' in dashboard.student_tabs:
        # Importeren plotly html in index html file
        student_name = student.email.split("@")[0].lower()
        file_name_html = instance.get_temp_path() + student_name + "_progress.html"
        student_tab_content['voortgang'] = '<h2 class="mt-2">Voortgang</h2>' + read_plotly(file_name_html)
    if 'portfolio' in dashboard.student_tabs:
        student_tab_content['portfolio'] = build_bootstrap_portfolio(instance, course_id, course, student,
                                                                     student_results, actual_date, actual_day,
                                                                     templates, dashboard.level_serie_collection)
    if 'feedback' in dashboard.student_tabs:
        student_tab_content['feedback'] = build_bootstrap_feedback(course, student_results, templates,
                                                                   dashboard.level_serie_collection)

    # print("BSI10 - ", student_tabs.keys())
    student_tabs_html_string = build_student_tabs(instance, course, student_tab_content,
                                                  dashboard.student_tabs)
    student_index_html_string = templates['student_index'].substitute(
        {
            'semester': course.name,
            'student_name': student.name,
            'student_email': student.email,
            'student_number': student.number,
            'project_group': project_group_name,
            'guild_group': guild_group_name,
            'project_group_teachers': project_group_teacher_str,
            'guild_group_teachers': guild_group_teacher_str,
            'actual_date': get_date_time_loc(actual_date),
            'student_tabs': student_tabs_html_string
        }
    )
    student_name = student.email.split("@")[0].lower()
    file_name_html = instance.get_student_path() + student_name + "_index.html"
    # print("BB21 - Write portfolio for", student.name)
    with open(file_name_html, mode='w', encoding="utf-8") as file_portfolio:
        file_portfolio.write(student_index_html_string)
    return

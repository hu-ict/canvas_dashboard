from scripts.lib.build_hover import get_hover_assignment, get_hover_grade, get_hover_status, get_comments_html, \
    get_rubrics_comments
from scripts.lib.lib_date import get_date_time_loc
from scripts.lib.lib_portfolio import STATUS_MISSED, STATUS_COMING, TOTAL_POINTS, STATUS_COMPLETE, STATUS_INCOMPLETE, \
    STATUS_PENDING
from scripts.model.perspective.Status import BEFORE_DEADLINE, MISSED_ITEM, VIEW_UNPOSTED, GRADED, NOT_YET_GRADED


def get_submission_badges(assignment_sequence, submission_sequence, actual_day, level_serie):
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
                if submission.get_status() == GRADED:
                    if submission.graded and submission.score == submission.assignment.points:
                        badge["status"] = level_serie.get_status(GRADED).color
                    else:
                        badge["status"] = level_serie.get_status(GRADED).color
                        # status = STATUS_INCOMPLETE
                else:
                    if submission.status is MISSED_ITEM:
                        badge["status"] = level_serie.get_status(MISSED_ITEM).color
                    else:
                        badge["status"] = level_serie.get_status(NOT_YET_GRADED).color

                badge["assignment_id"] = assignment.id
                badge["teller"] = teller
                badges.append(badge)
            else:
                if actual_day > assignment.day:
                    teller += 1
                    badge = {}
                    badge["status"] = level_serie.get_status(MISSED_ITEM).color
                    badge["assignment_id"] = assignment.id
                    badge["teller"] = teller
                    badges.append(badge)
                else:
                    teller += 1
                    badge = {}
                    badge["status"] = level_serie.get_status(BEFORE_DEADLINE).color
                    badge["assignment_id"] = assignment.id
                    badge["teller"] = teller
                    badges.append(badge)
        else:
            if actual_day > assignment.day:
                teller += 1
                badge = {}
                badge["status"] = level_serie.get_status(MISSED_ITEM).color
                badge["assignment_id"] = assignment.id
                badge["teller"] = teller
                badges.append(badge)
            else:
                teller += 1
                badge = {}
                badge["status"] = level_serie.get_status(BEFORE_DEADLINE).color
                badge["assignment_id"] = assignment.id
                badge["teller"] = teller
                badges.append(badge)
    return badges


def get_portfolio_item(course, student_results, assignment_sequence, actual_day, feedback_colors, level_serie, templates):
    # ********************************
    # Start portfolio item in matrix
    # ********************************
    portfolio_item_name = assignment_sequence.name + " (" + str(len(assignment_sequence.assignments)) + ")"
    submission_sequence = student_results.get_submission_sequence_by_name(assignment_sequence.name)

    # *********************************
    # date color
    # *********************************
    date, day = assignment_sequence.get_date_day(submission_sequence, actual_day)
    if day < actual_day:
        background_color = "#ffb3b3"
    else:
        background_color = "#c6ecd9"

    # *********************************
    # Status- and Grade-labels and -colors
    # *********************************
    comment_label = ""
    comment_color = "white"
    if submission_sequence is None:
        # No submissions
        portfolio_item_date, portfolio_item_day = assignment_sequence.get_date_day(submission_sequence, actual_day)
        if actual_day <= portfolio_item_day:
            status_label = level_serie.get_status(BEFORE_DEADLINE).label
            status_color = level_serie.get_status(BEFORE_DEADLINE).color
        else:
            status_label = level_serie.get_status(MISSED_ITEM).label
            status_color = level_serie.get_status(MISSED_ITEM).color
        grade_label = ""
        grade_color = "white"
    else:
        if submission_sequence.is_posted() or VIEW_UNPOSTED:
            if submission_sequence.is_graded():
                grade_label = level_serie.get_grades(submission_sequence.get_grade()).label
                grade_color = level_serie.get_grades(submission_sequence.get_grade()).color
            else:
                grade_label = ""
                grade_color = "white"
            if submission_sequence.is_late():
                comment_label = "Te laat"
                comment_color = "white"
        else:
            grade_label = "Niet gepubliceerd"
            grade_color = "white"
        status_label = level_serie.get_status(submission_sequence.get_status()).label
        status_color = level_serie.get_status(submission_sequence.get_status()).color

    # **********************************
    # Bouw de badge met de Canvas link
    # **********************************
    badges = get_submission_badges(assignment_sequence, submission_sequence, actual_day, level_serie)
    submission_badges = ""
    for badge in badges:
        url = "https://canvas.hu.nl/courses/" + str(
            course.canvas_id) + "/gradebook/speed_grader?assignment_id=" + str(badge["assignment_id"]) + "&student_id=" + str(student_results.id)
        submission_badges += '<a class="badge mr-1" style="color: white; background-color: ' + badge["status"] + '" target="_blank" href="' + url + '">' + str(
            badge["teller"]) + '</a>'

    # **********************************
    # Bouw het modal window met feedback
    # **********************************
    modal_content_html_string = ""
    portfolio_items_modal_html_string = ""
    if submission_sequence is not None:
        for submission in submission_sequence.submissions:
            # bouw de teksten voor het modal scherm
            modal_content_html_string += "<p>"
            modal_content_html_string += get_hover_assignment(True, submission)
            if submission.graded and VIEW_UNPOSTED:
                grade = level_serie.grades[submission.grade]
                modal_content_html_string += get_hover_grade(course, submission, grade)
                modal_content_html_string += get_rubrics_comments(course, submission, grade, False)
            else:
                status = level_serie.status[submission.status]
                modal_content_html_string += get_hover_status(submission, status)
            if submission.posted or VIEW_UNPOSTED:
                modal_content_html_string += get_comments_html(submission.comments)
            modal_content_html_string += "</p>"
        portfolio_items_modal_html_string += templates['portfolio_item_modal'].substitute(
            {"portfolio_item_id": assignment_sequence.tag,
             "portfolio_item": portfolio_item_name,
             "content": modal_content_html_string})
        portfolio_items_modal_html_string += '<a class="badge btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#target' + assignment_sequence.tag + '"' + " onclick='scrollToTop()'>Detail</a>"

    portfolio_item_dict = {
        "portfolio_item": portfolio_item_name,
        "portfolio_item_id": assignment_sequence.tag,
        "portfolio_item_modal": portfolio_items_modal_html_string,
        "submission_badges": submission_badges,
        "portfolio_date": get_date_time_loc(date),
        "portfolio_day": day,
        "background_color": background_color,
        "portfolio_status_color": status_color,
        "portfolio_status_label": status_label,
        "portfolio_grade_color": grade_color,
        "portfolio_grade_label": grade_label,
        "portfolio_comment_color": comment_color,
        "portfolio_comment_label": comment_label
    }
    # *********************************
    # Learning outcome observations
    # *********************************
    learning_outcomes_row_html_string = ""
    if submission_sequence is not None:
        if submission_sequence.is_posted() or VIEW_UNPOSTED:
            for learning_outcome in course.learning_outcomes:
                learning_outcomes_row_html_string += '<td style="text-align:center;">'
                for submission in submission_sequence.submissions:
                    for feedback in submission.learning_outcomes[learning_outcome.id].feedback_list:
                        learning_outcomes_row_html_string += '<span class="badge badge-primary" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-custom-class="competentie-tooltip" title="' + feedback.comment + '" style="background-color:  ' + \
                                                             feedback_colors[
                                                                 feedback.positive_neutral_negative][
                                                                 "color"] + ';">' + feedback.positive_neutral_negative + '</span>'
                learning_outcomes_row_html_string += '</td>'
        else:
            for learning_outcome in course.learning_outcomes:
                learning_outcomes_row_html_string += '<td></td>'
    else:
        for learning_outcome in course.learning_outcomes:
            learning_outcomes_row_html_string += '<td></td>'
    portfolio_item_dict["learning_outcomes"] = learning_outcomes_row_html_string
    return portfolio_item_dict

def get_observation_item(course, student_results, assignment_sequence, learning_outcome, feedback, actual_day, feedback_colors, level_serie, templates):
    # ********************************
    # Start portfolio item in matrix
    # ********************************
    portfolio_item_name = feedback.assignment_name

    # *********************************
    # date color
    # *********************************
    background_color = "#ffb3b3"

    # *********************************
    # Status- and Grade-labels and -colors
    # *********************************
    status_label = "Gepubliceerd"
    status_color = "#3C7D22"
    grade_label = ""
    grade_color = "white"
    comment_label = ""
    comment_color = "white"

    # **********************************
    # Bouw de badge met de Canvas link
    # **********************************
    submission_sequence = student_results.get_submission_sequence_by_name(assignment_sequence.name)
    badges = get_submission_badges(assignment_sequence, submission_sequence, actual_day, level_serie)
    submission_badges = ""
    for badge in badges:
        url = "https://canvas.hu.nl/courses/" + str(
            course.canvas_id) + "/gradebook/speed_grader?assignment_id=" + str(badge["assignment_id"]) + "&student_id=" + str(student_results.id)
        submission_badges += '<a class="badge mr-1" style="color: white; background-color: ' + badge["status"] + '" target="_blank" href="' + url + '">' + str(
            badge["teller"]) + '</a>'


    modal_content_html_string = ""
    # **********************************
    # Bouw het modal window met feedback
    # **********************************
    portfolio_items_modal_html_string = ""
    # if submission_sequence is not None:
    #     for submission in submission_sequence.submissions:
    #         # bouw de teksten voor het modal scherm
    #         modal_content_html_string += "<p>"
    #         modal_content_html_string += get_hover_assignment(True, submission)
    #         if submission.graded and VIEW_UNPOSTED:
    #             grade = level_serie.grades[submission.grade]
    #             modal_content_html_string += get_hover_grade(course, submission, grade)
    #             modal_content_html_string += get_rubrics_comments(course, submission, grade)
    #         else:
    #             status = level_serie.status[submission.status]
    #             modal_content_html_string += get_hover_status(submission, status)
    #         if submission.posted or VIEW_UNPOSTED:
    #             modal_content_html_string += get_comments_html(submission.comments)
    #         modal_content_html_string += "</p>"
    #     portfolio_items_modal_html_string += templates['portfolio_item_modal'].substitute(
    #         {"portfolio_item_id": assignment_sequence.tag,
    #          "portfolio_item": portfolio_item_name,
    #          "content": modal_content_html_string})
    #     portfolio_items_modal_html_string += '<a class="badge btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#target' + assignment_sequence.tag + '"' + " onclick='scrollToTop()'>Detail</a>"

    portfolio_item_dict = {
        "portfolio_item": portfolio_item_name,
        "portfolio_item_id": feedback.assignment_id,
        "portfolio_item_modal": portfolio_items_modal_html_string,
        "submission_badges": submission_badges,
        "portfolio_date": get_date_time_loc(feedback.date),
        "portfolio_day": feedback.day,
        "background_color": background_color,
        "portfolio_status_color": status_color,
        "portfolio_status_label": status_label,
        "portfolio_grade_color": grade_color,
        "portfolio_grade_label": grade_label,
        "portfolio_comment_color": comment_color,
        "portfolio_comment_label": comment_label
    }
    # *********************************
    # Learning outcome observations
    # *********************************
    learning_outcomes_row_html_string = ""

    for learning_outcome_item in course.learning_outcomes:
        learning_outcomes_row_html_string += '<td style="text-align:center;">'
        if learning_outcome_item.id == learning_outcome.id:
            learning_outcomes_row_html_string += '<span class="badge badge-primary" data-bs-toggle="tooltip" data-bs-placement="right" data-bs-custom-class="competentie-tooltip" title="' + feedback.comment + '" style="background-color:  ' + \
                                                     feedback_colors[
                                                         feedback.positive_neutral_negative][
                                                         "color"] + ';">' + feedback.positive_neutral_negative + '</span>'
        learning_outcomes_row_html_string += '</td>'

    portfolio_item_dict["learning_outcomes"] = learning_outcomes_row_html_string
    return portfolio_item_dict


def build_bootstrap_prop_portfolio(course_id, course, student, student_results, actual_day, templates, level_serie_collection):
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

                badges = get_submission_badges(assignment_sequence, submission_sequence, actual_day, level_serie)
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
    return learning_outcome_totals, portfolio_items

from scripts.lib.build_bootstrap_student_button import build_student_button
from scripts.lib.build_plotly_learning_analytics import build_plotly_learning_analytics
from scripts.lib.file import read_plotly
from scripts.lib.lib_date import get_date_time_loc
from scripts.model.dashboard.LevelSerie import STR_GRADES, STR_STATUS


def build_bootstrap_learning_analytics_index_html(assigment_learning_analytics, course, results, assignment, a_level_serie_collection, templates, plotly_file_name, index_file_name):
    status_html = ""
    status_list = assigment_learning_analytics["status"]
    assignment_group = course.get_assignment_group_by_assignment(assignment.id)
    for status_level in status_list:
        submission_html = ""
        for submission in assigment_learning_analytics["status"][status_level]["items"]:
            result_student = results.find_student(submission.student_id)
            role = course.get_role(result_student.role)
            if role is not None:
                url = ("https://canvas.hu.nl/courses/" + str(
                    course.canvas_id) + "/gradebook/speed_grader?assignment_id=" +
                       str(assignment.id) + "&student_id=" + str(result_student.id))
                submission_html += build_student_button(role.btn_color, result_student, "_blank", url, templates,
                                                        a_level_serie_collection)
            else:
                print("BBDI21 - role for student is NoneType", result_student)
        level_serie = a_level_serie_collection.level_series[assignment_group.levels]
        status_str = level_serie.status[status_level].label
        status_html += templates["analytics_assignment_status"].substitute(
            {"status": status_str,
             "count": assigment_learning_analytics["status"][status_level]["count"],
             "assignments": submission_html}
        )
    grade_html = ""
    grade_list = assigment_learning_analytics[STR_GRADES]


    for grade_level in grade_list:
        submission_html = ""
        for submission in assigment_learning_analytics[STR_GRADES][grade_level]["items"]:
            result_student = results.find_student(submission.student_id)
            # print('BB07 -', l_student.name, "[", l_student.number, "]")
            role = course.get_role(result_student.role)
            if role is not None:
                url = ("https://canvas.hu.nl/courses/" + str(
                    course.canvas_id) + "/gradebook/speed_grader?assignment_id=" +
                       str(assignment.id) + "&student_id=" + str(result_student.id))
                submission_html += build_student_button(role.btn_color, result_student, "_blank", url, templates, a_level_serie_collection)
            else:
                print("BBDI21 - role for student is NoneType", result_student)


            # submission_html += templates["analytics_assignment_item"].substitute(
            #     {"url": url,
            #      "student_name": student.name,
            #      "submission_date": get_date_time_loc(submission.submitted_date)}
            # )
        level_serie = a_level_serie_collection.level_series[assignment_group.levels]
        if grade_level in level_serie.grades:
            grade_str = level_serie.grades[grade_level].label
            grade_html += templates["analytics_assignment_status"].substitute(
                {"status": grade_str,
                 "count": assigment_learning_analytics[STR_GRADES][grade_level]["count"],
                 "assignments": submission_html}
            )

    html_string = templates["analytics_index"].substitute(
        {'analytics_name': assignment.name,
         'overview': read_plotly(plotly_file_name),
         'status': status_html,
         'value': grade_html})
    # print("BB21 - Write portfolio for", student.name)
    with open(index_file_name, mode='w', encoding="utf-8") as file:
        file.write(html_string)

    return

def build_learning_analytics_dict(course, results, level_serie_collection):
    learning_analytics = {}
    for assignment_group in course.assignment_groups:
        perspective = course.find_perspective_by_assignment_group(assignment_group.id)
        if perspective is not None:
            grades = level_serie_collection.level_series[assignment_group.levels].grades
            for assignment_sequence in assignment_group.assignment_sequences:
                for assignment in assignment_sequence.assignments:
                    grades_dict = {}
                    for grade in grades.keys():
                        grades_dict[grade] = {"count": 0, "items": []}
                    learning_analytics[str(assignment.id)] = {"assignment": assignment.id,
                                                              "assignment_name": assignment.name,
                                                              "level_serie": assignment_group.levels,
                                                              STR_STATUS: {"1": {"count": 0, "items": []},
                                                                           "2": {"count": 0, "items": []},
                                                                           "3": {"count": 0, "items": []},
                                                                           "4": {"count": 0, "items": []},
                                                                           "5": {"count": 0, "items": []}},
                                                              STR_GRADES: grades_dict}

    for student in results.students:
        # print(l_peil_construction)
        # print("GL10 -", student.name)
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    learning_analytics[str(submission.assignment.id)][STR_STATUS][str(submission.status)]["count"] += 1
                    learning_analytics[str(submission.assignment.id)][STR_STATUS][str(submission.status)]["items"].append(submission)
                    if submission.grade is not None:
                        learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)]["count"] += 1
                        learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)]["items"].append(submission)

        for submission in student.student_level_moments.submissions:
            learning_analytics[str(submission.assignment.id)][STR_STATUS][str(submission.status)]["count"] += 1
            learning_analytics[str(submission.assignment.id)][STR_STATUS][str(submission.status)]["items"].append(submission)
            if submission.grade is not None:
                # print("BLA02 -", submission.assignment.name, submission.assignment.id, submission.grade)
                learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)]["count"] += 1
                learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)]["items"].append(submission)
        for submission in student.student_grade_moments.submissions:
            learning_analytics[str(submission.assignment.id)][STR_STATUS][str(submission.status)]["count"] += 1
            learning_analytics[str(submission.assignment.id)][STR_STATUS][str(submission.status)]["items"].append(submission)
            if submission.grade is not None:
                # print("BLA03 -", submission.assignment.name, submission.assignment.id, submission.grade)
                learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)]["count"] += 1
                learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)]["items"].append(submission)
    return learning_analytics

def get_learning_analytics_from_results(results):
    learning_analytics = {}
    for student in results.students:
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    learning_analytics[str(submission.assignment.id)]["status"][str(submission.status)] += 1
                    if submission.grade is not None:
                        learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)] += 1



def build_bootstrap_learning_analytics_tab(course_instance, a_course, a_results, learning_analytics, a_templates, a_level_serie_collection,
                                  actual_day):
    html_string = ""
    for assignment_group in a_course.assignment_groups:
        assignment_html_string = ""
        assignment_list = []
        for assignment_sequence in assignment_group.assignment_sequences:
            for assignment in assignment_sequence.assignments:
                assignment_list.append(assignment)
        assignment_list = sorted(assignment_list, key=lambda a: a.day)
        for assignment in assignment_list:
            index_file_name = "analytics_" + str(assignment.id).lower() + ".html"
            plotly_file_name = "plotly_analytics_" + str(assignment.id).lower() + ".html"
            link_path_name = course_instance.get_link_general_path() + index_file_name

            if assignment.day < actual_day:
                background_color = "#ffb3b3"
            else:
                background_color = "#c6ecd9"
            assignment_html_string += a_templates["analytics_assignment"].substitute(
                {'url': link_path_name,
                 'assignment_name': assignment.name,
                 'background_color': background_color,
                 'assignment_lock_date': get_date_time_loc(
                     assignment.date)})
            build_plotly_learning_analytics(learning_analytics, assignment, a_level_serie_collection,
                              course_instance.get_html_general_path() + plotly_file_name)
            assignment_learning_analytics = learning_analytics[str(assignment.id)]

            build_bootstrap_learning_analytics_index_html(assignment_learning_analytics, a_course, a_results, assignment, a_level_serie_collection, a_templates,
                                                          course_instance.get_html_general_path() + plotly_file_name,
                                                          course_instance.get_html_general_path() + index_file_name)

        html_string += a_templates["analytics_card"].substitute({'assignment_group_id': str(assignment.group_id),
                                                                 'assignment_group_name': assignment_group.name,
                                                                 'assignments': assignment_html_string})
    return html_string

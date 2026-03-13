from scripts.lib.build_plotly_analyse import process_analytics
from scripts.lib.lib_date import get_date_time_loc
from scripts.model.dashboard.LevelSerie import STR_GRADES


def build_learning_analytics(course, results, level_serie_collection):
    learning_analytics = {}
    for assignment_group in course.assignment_groups:
        perspective = course.find_perspective_by_assignment_group(assignment_group.id)
        if perspective is not None:
            grades = level_serie_collection.level_series[assignment_group.levels].grades
            for assignment_sequence in assignment_group.assignment_sequences:
                for assignment in assignment_sequence.assignments:
                    grades_dict = {}
                    for grade in grades.keys():
                        grades_dict[grade] = 0
                    learning_analytics[str(assignment.id)] = {"assignment": assignment.id,
                                                              "assignment_name": assignment.name,
                                                              "level_serie": assignment_group.levels,
                                                              "status": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
                                                              STR_GRADES: grades_dict}

    for student in results.students:
        # print(l_peil_construction)
        # print("GL10 -", student.name)
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                for submission in submission_sequence.submissions:
                    learning_analytics[str(submission.assignment.id)]["status"][str(submission.status)] += 1
                    if submission.grade is not None:
                        learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)] += 1
        for submission in student.student_level_moments.submissions:
            learning_analytics[str(submission.assignment.id)]["status"][str(submission.status)] += 1
            if submission.grade is not None:
                # print("BLA02 -", submission.assignment.name, submission.assignment.id, submission.grade)
                learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)] += 1
        for submission in student.student_grade_moments.submissions:
            learning_analytics[str(submission.assignment.id)]["status"][str(submission.status)] += 1
            if submission.grade is not None:
                # print("BLA03 -", submission.assignment.name, submission.assignment.id, submission.grade)
                learning_analytics[str(submission.assignment.id)][STR_GRADES][str(submission.grade)] += 1
    return learning_analytics


def build_bootstrap_learning_analytics_tab(course_instance, a_course, learning_analytics, a_templates, a_level_serie_collection,
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
            file_name = "analytics_" + str(assignment.id).lower() + ".html"
            link_path_name = course_instance.get_link_general_path() + file_name

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
            process_analytics(learning_analytics, assignment, a_level_serie_collection,
                              course_instance.get_html_general_path() + file_name)

        html_string += a_templates["analytics_card"].substitute({'assignment_group_id': str(assignment.group_id),
                                                                 'assignment_group_name': assignment_group.name,
                                                                 'assignments': assignment_html_string})
    return html_string

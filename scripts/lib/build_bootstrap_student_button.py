def build_student_button(btn_color, result_student, target, url, templates, level_serie_collection):


    l_progress_color = level_serie_collection.level_series['progress'].grades[str(result_student.get_saturation())].color
    bof_count = 0
    # for learning_outcome in student.learning_outcomes.values():
    #     bof_count += len(learning_outcome.feedback_list)
    # if bof_count == 0:
    #     bof_count_str = ""
    # else:
    #     bof_count_str = str(bof_count)
    return templates['student'].substitute(
        {'btn_color': btn_color,
         'progress_color': l_progress_color,
         'student_name': result_student.name,
         'student_number': result_student.number,
         'student_role': "Berend",
         'bof_count': "",
         'target': target,
         'url': url
         })


def build_student_button1(course, student, templates, labels_colors):
    role = course.get_role(student.role)
    if not role:
        return ""
    color = role.btn_color
    l_progress_color = labels_colors.level_series['progress'].levels["-1"].color
    return templates['student'].substitute(
        {'btn_color': color, 'progress_color': l_progress_color, 'student_name': student.name,
         'student_role': role.name, 'student_file': "asci_file_name"})
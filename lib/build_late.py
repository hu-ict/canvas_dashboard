from operator import itemgetter
from lib.lib_date import get_date_time_loc, get_date_time_obj


def build_bootstrap_late_submission_item(a_templates, a_result, l_submission):
    student_id = l_submission['student_id']
    # print("BL22 -", l_submission, student_id)
    l_student_name = a_result.find_student(student_id).name
    l_messages = l_submission['messages']
    if len(l_messages) > 0:
        messages = l_messages[0]
    else:
        messages = ""
    url = "https://canvas.hu.nl/courses/" + str(a_result.id) + "/gradebook/speed_grader?assignment_id=" + str(
        l_submission['assignment_id']) + "&student_id=" + str(l_submission['student_id'])
    submission_html_string = a_templates["submission"].substitute(
        {'submission_id': l_submission['id'], 'student_name': l_student_name,
         'assignment_name': l_submission['assignment_name'],
         'submission_date': get_date_time_loc(get_date_time_obj(l_submission['submitted_date'])), 'url': url,
         'messages': messages})
    return submission_html_string


def build_bootstrap_teacher_index(a_instance, a_templates, a_course, a_result, a_workload):
    for workload_teacher in a_workload.workload_teachers:
        late_list_temp = workload_teacher.worklist
        late_list = sorted(late_list_temp, key=itemgetter('submitted_date'))
        late_list_html_total_string = ''
        for l_submission in late_list:
            # if l_submission["submitted_day"]+7 < a_result.actual_day:
            #     print("BL22 -", l_submission)
            late_item = build_bootstrap_late_submission_item(a_templates, a_result, l_submission)
            late_list_html_total_string += late_item
            if l_submission["submitted_day"] is None:
                day = a_course.days_in_semester
            else:
                day = l_submission["submitted_day"]
            item = {"submitted_day": day, "item": late_item}
        workload_html_string = a_templates["teacher_workload"].substitute({'submissions': late_list_html_total_string})
        # teacher_html_string = a_templates["teacher_teacher"].substitute({'teacher_name': teacher.name})
        teacher = a_course.find_teacher_by_initials(workload_teacher.initials)
        groups = dict()
        for responsibility in teacher.responsibilities:
            if responsibility.student_group_collection == "project_groups":
                groups["Projectgroepen"] = dict()
                break
        for responsibility in teacher.responsibilities:
            if responsibility.student_group_collection == "guild_groups":
                groups["Gildegroepen"] = dict()
                break
        for responsibility in teacher.responsibilities:
            if responsibility.student_group_collection == "project_groups":
                for student_group_name in responsibility.student_groups:
                    group_name = a_course.find_project_group_by_name(student_group_name).name
                    assignment_group = a_course.get_assignment_group(responsibility.assignment_group_id)
                    if group_name in groups["Projectgroepen"]:
                        groups["Projectgroepen"][group_name] += ", "+assignment_group.name
                    else:
                        groups["Projectgroepen"][group_name] = "Opdrachtgroepen: "+assignment_group.name

            elif responsibility.student_group_collection == "guild_groups":
                for student_group_name in responsibility.student_groups:
                    group_name = a_course.find_guild_group_by_name(student_group_name).name
                    assignment_group = a_course.get_assignment_group(responsibility.assignment_group_id)
                    if group_name in groups["Gildegroepen"]:
                        groups["Gildegroepen"][group_name] += ", "+assignment_group.name
                    else:
                        groups["Gildegroepen"][group_name] = "Opdrachtgroepen: "+assignment_group.name
            teacher_html_string = "<ul>"
            for item in groups:
                teacher_html_string += "<li>"+item
                teacher_html_string += "<ul>"
                for item_n1 in groups[item]:
                    teacher_html_string += "<li>"+item_n1
                    teacher_html_string += "<ul><li>" + groups[item][item_n1] + "</li></ul>"
                    teacher_html_string += "</li>"
                teacher_html_string += "</ul>"
                teacher_html_string += "</li>"
            teacher_html_string += "</ul>"

        teacher_index_html = a_templates["teacher_index"].substitute({'teacher_id': teacher.initials, 'teacher_name': teacher.name, 'workload': workload_html_string, 'teacher': teacher_html_string})

        file_name = "teacher_"+teacher.initials+".html"
        with open(a_instance.get_html_path()+file_name, mode='w', encoding="utf-8") as file_late_list:
            file_late_list.write(teacher_index_html)


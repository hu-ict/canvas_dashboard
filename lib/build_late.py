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


def build_bootstrap_late_submission_list(a_instance, a_templates, a_course, a_result, a_workload):
    for teacher in a_workload.workload_teachers:
        late_list_temp = teacher.worklist
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
        late_list_html_string = a_templates["late_list"].substitute({'submissions': late_list_html_total_string})
        file_name = "late_"+teacher.initials+".html"
        with open(a_instance.get_html_path()+file_name, mode='w', encoding="utf-8") as file_late_list:
            file_late_list.write(late_list_html_string)


import json
import sys

from scripts.lib.file import read_course, read_msteams_api, read_environment
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, MSTEAMS_API_KEY_FILE_NAME
from scripts.lib.lib_date import get_actual_date

def update_sites_from_json(course_code, instance_name):
    print("USJ01 - update_sites_from_json.py", instance_name)
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    print("USJ03 - update_sites.py", ENVIRONMENT_FILE_NAME)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    print("Instance:", course_instance.name)

    if course_instance.course_code not in ["TICT-V3SE6-25"]:
        print("US04 - No student channels defined for this course")
        return
    course = read_course(course_instance.get_course_file_name())
    msteams_api = read_msteams_api(MSTEAMS_API_KEY_FILE_NAME)
    print("USJ06 -", len(msteams_api.channels))
    for student in course.students:
        print("USJ11 -", student.name, student.id)
        channel = msteams_api.get_channel_by_student(student.id)
        # print("USJ11 -", channel)
        if channel is not None:
            student.site = channel.channel
        else:
            print("USJ12 - Student niet gevonden", student.name)

    with open(course_instance.get_course_file_name(), 'w') as f:
        dict_result = course.to_json()
        json.dump(dict_result, f, indent=2)

    print("USJ99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_sites_from_json(sys.argv[1], sys.argv[2])
    else:
        update_sites_from_json("", "")

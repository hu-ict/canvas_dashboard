import json
import sys

from scripts.lib.file import read_course, read_msteams_api, read_environment
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, MSTEAMS_API_KEY_FILE_NAME
from scripts.lib.lib_date import get_actual_date

def update_sites_from_json(course_code, instance_name):
    sys.stdout.reconfigure(encoding="utf-8")
    print("USJ01 - update_sites_from_json.py", instance_name)
    g_actual_date = get_actual_date()
    print("PSF01 - publish_student_files.py")
    g_actual_date = get_actual_date()
    print("PSF02 -", ENVIRONMENT_FILE_NAME, course_code)
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    execution = environment.get_execution_by_name("env_3")
    course_instance = environment.get_instance_of_course(environment.current_instance)
    course_instance.execution_source_path = execution.source_path
    print("PSF03 -", environment)
    print("PSF04 - Instance:", course_instance.name)
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

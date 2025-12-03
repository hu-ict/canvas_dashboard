import json
import sys

from lib.file import read_course, read_msteams_api, read_course_instances, read_environment
from lib.lib_date import get_actual_date
from lib.teams_api_lib import upload_file_to_onedrive, get_me_for_check, get_access_token
from model.environment.Environment import ENVIRONMENT_FILE_NAME


def publish_student_files(course_code, instance_name):
    print("PSF01 - publish_student_files.py")
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    print("Instance:", course_instance.name)

    course = read_course(course_instance.get_course_file_name())
    msteams_api = read_msteams_api("msteams_api.json")
    if get_me_for_check(msteams_api.gen_token) is None:
        token = get_access_token(msteams_api.tenant_id, msteams_api.client_id)
        print(token)
        msteams_api.gen_token = token
        with open("msteams_api.json", 'w') as f:
            dict_result = msteams_api.to_json()
            json.dump(dict_result, f, indent=2)

    for l_student in course.students:
        if l_student.site is not None:
            print('PSF02 Upload files for Student:', l_student.name)
            student_name = l_student.email.split("@")[0].lower()
            source_filename = student_name + "_progress.jpg"
            upload_file_to_onedrive(msteams_api.gen_token, student_name, l_student.site, course_instance.get_html_student_path(),
                                    source_filename)
            source_filename = student_name + "_index.html"
            upload_file_to_onedrive(msteams_api.gen_token, student_name, l_student.site, course_instance.get_html_student_path(),
                                    source_filename)
        else:
            print("PSF04 MSTeams channel not defined (site)")

    print("PSF99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        publish_student_files(sys.argv[1], sys.argv[2])
    else:
        publish_student_files("", "")

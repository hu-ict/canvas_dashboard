import sys

from lib.file import read_course, read_msteams_api, read_course_instances
from lib.lib_date import get_actual_date
from lib.teams_api_lib import upload_file_to_onedrive


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("PB02 - Instance:", instance.name)

    course = read_course(instance.get_course_file_name())
    msteams_api = read_msteams_api("msteams_api.json")
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    for l_student in course.students:
        if l_student.site is not None:
            print('PS02 Upload files for Student:', l_student.name)
            student_name = l_student.email.split("@")[0].lower()
            source_filename = student_name + "_progress.jpg"

            upload_file_to_onedrive(msteams_api.my_token, l_student.name, l_student.site, instance.get_student_path(),
                                    source_filename)
            # source_filename = l_student.name + "_progress.html"
            # upload_file_to_onedrive(msteams_api.my_token, l_student.name, l_student.site, instance.get_student_path(),
            #                         source_filename)
            source_filename = student_name + "_index.html"
            upload_file_to_onedrive(msteams_api.my_token, l_student.name, l_student.site, instance.get_student_path(),
                                    source_filename)
        else:
            print("PS04 MSTeams channel not defined (site)")

    print("PS99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

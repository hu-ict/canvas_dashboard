import sys

from lib.file import read_start, read_course, read_msteams_api, read_course_instance
from lib.lib_date import get_actual_date
from lib.teams_api_lib import upload_file_to_onedrive


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("PS01 Instance:", instances.current_instance)
    course = read_course(instances.get_course_file_name(instances.current_instance))
    msteams_api = read_msteams_api("msteams_api.json")
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    for l_student in course.students:
        if l_student.site is not None:
            print('PS02 Upload files for Student:', l_student.name)
            source_filename = l_student.name + " progress.jpeg"
            upload_file_to_onedrive(msteams_api.my_token, l_student.name, l_student.site, instances.get_student_path(), source_filename)
            source_filename = l_student.name + " progress.html"
            upload_file_to_onedrive(msteams_api.my_token, l_student.name, l_student.site, instances.get_student_path(), source_filename)
            source_filename = l_student.name + " index.html"
            upload_file_to_onedrive(msteams_api.my_token, l_student.name, l_student.site, instances.get_student_path(), source_filename)
            # source_filename = l_student.name + " portfolio.html"
            # upload_file_to_onedrive(msteams_api.my_token, l_student.name, l_student.site, instances.get_student_path(), source_filename)
        else:
            print("PS04 MSTeams channel not defined (site)")

    print("PS99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

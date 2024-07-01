import sys

from lib.file import read_start, read_course, read_msteams_api, read_course_instance
from lib.lib_date import get_actual_date
from lib.teams_api_lib import upload_file_html, upload_file_jpeg



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
            print('PS02 HTML, JPEG Student:', l_student.name)
            upload_file_html(msteams_api.my_token, instances.get_plot_path(), l_student.name, l_student.site)
            upload_file_jpeg(msteams_api.my_token, instances.get_plot_path(), l_student.name, l_student.site)
        else:
            print("PS04 MSTeams channel not defined (site)")
    print("PS99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

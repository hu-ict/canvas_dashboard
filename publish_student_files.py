from lib.file import read_start, read_course, read_msteams_api, read_course_instance
from lib.teams_api_lib import upload_file_html, upload_file_jpeg

instances = read_course_instance()
print("Instance:", instances.current_instance)
start = read_start(instances.get_start_file_name())
course = read_course(start.course_file_name)
msteams_api = read_msteams_api("msteams_api.json")

for l_student in course.students:
    if l_student.site is not None:
        print('HTML, JPEG Student:', l_student.name)
        upload_file_html(msteams_api.my_token, instances.get_plot_path(), l_student.name, l_student.site)
        upload_file_jpeg(msteams_api.my_token, instances.get_plot_path(), l_student.name, l_student.site)
    else:
        print("MSTeams channel not defined (site)")
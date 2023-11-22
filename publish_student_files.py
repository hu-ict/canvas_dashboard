from lib.file import read_start, read_course, read_msteams_api, plot_path
from lib.teams_api_lib import upload_file_html, upload_file_jpeg

start = read_start()
course = read_course(start.course_file_name)
msteams_api = read_msteams_api("msteams_api.json")

for l_student in course.students:
    print('HTML, JPEG Student:', l_student.name)
    upload_file_html(msteams_api.my_token, plot_path, l_student.name, l_student.site)
    upload_file_jpeg(msteams_api.my_token, plot_path, l_student.name, l_student.site)



import json
import shutil
import sys

from scripts.lib.file import read_environment
from lib.lib_date import get_actual_date
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, DIR_DIV


def publish_dashboard(course_code, instance_name):
    print("PDB01 - publish_dashboard.py")
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    print("Instance:", course_instance.name)

    print("PDB91 - Copy files to OneDrive docenten")
    file_names = []
    file_names.append("index.html")
    for file_name in file_names:
        shutil.copyfile(course_instance.get_html_index_path() + file_name, course_instance.target_path + file_name)
        # print(file_name)
    print("PDB92 - Target", course_instance.target_path + course_instance.name + DIR_DIV + "students")
    shutil.copytree(course_instance.get_html_student_path(), course_instance.target_path + course_instance.name + DIR_DIV + "students", copy_function=shutil.copy2,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)
    print("PDB93 - Target", course_instance.target_path + course_instance.name + DIR_DIV + "general")
    shutil.copytree(course_instance.get_html_general_path(), course_instance.target_path + course_instance.name + DIR_DIV + "general", copy_function=shutil.copy2,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)
    print("PDB99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        publish_dashboard(sys.argv[1], sys.argv[2])
    else:
        publish_dashboard("", "")

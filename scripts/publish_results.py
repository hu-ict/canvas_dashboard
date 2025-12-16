import json
import shutil
import sys

from scripts.lib.file import read_environment
from lib.lib_date import get_actual_date
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME


def publish_results(course_code, instance_name):
    print("PRS01 - publish_results.py")
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    print("Instance:", course_instance.name)

    print("PRS11 - Copy files to another environment")
    file_names = []
    file_names.append("dashboard_"+course_instance.name+".json")
    file_names.append("course_"+course_instance.name+".json")
    file_names.append("results_"+course_instance.name+".json")
    file_names.append("progress_"+course_instance.name+".json")
    file_names.append("workload_"+course_instance.name+".json")

    for file_name in file_names:
        shutil.copyfile(course_instance.get_html_index_path() + file_name, course_instance.target_path + file_name)
        # print(file_name)
    print("PDB93 - Target", course_instance.get_project_path + course_instance.name + "//general")
    shutil.copytree(course_instance.get_project_path(), course_instance.target_path + course_instance.name + "//general", copy_function=shutil.copy2,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)
    print("PRS99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        publish_results(sys.argv[1], sys.argv[2])
    else:
        publish_results("", "")
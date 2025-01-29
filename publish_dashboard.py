import shutil
import sys

from lib.file import read_start, read_course_instances
from lib.lib_date import get_actual_date


def publish_dashboard(instance_name):
    print("PB01 publish_dashboard.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("PB02 - Instance:", instance.name)
    start = read_start(instance.get_start_file_name())
    print("PB04 - Copy files to OneDrive docenten")
    file_names = []
    file_names.append("index.html")
    for file_name in file_names:
        shutil.copyfile(instance.get_html_root_path() + file_name, start.target_path + file_name)
        # print(file_name)
    shutil.copytree(instance.get_student_path(), start.target_path + instance_name + "//students", copy_function=shutil.copy2,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)
    shutil.copytree(instance.get_html_path(), start.target_path + instance_name + "//general", copy_function=shutil.copy2,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)
    print("PD99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        publish_dashboard(sys.argv[1])
    else:
        publish_dashboard("")

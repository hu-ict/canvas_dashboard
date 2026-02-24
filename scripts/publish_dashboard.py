import shutil

from scripts.lib.lib_date import get_actual_date
from scripts.lib.file_const import DIR_DIV


def publish_dashboard(course_instance):
    print("PDB01 - publish_dashboard.py")
    g_actual_date = get_actual_date()
    print("PDB91 - Copy files to OneDrive docenten")
    file_names = ["index.html"]
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


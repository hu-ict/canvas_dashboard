import shutil
import sys

from lib.file import read_start, read_course_instance
from lib.lib_date import get_actual_date


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    print("Copy files to OneDrive docenten")
    if instances.is_instance_of("inno_courses"):
        file_names = ["index.html", "late.html",
                      "late_gilde_BIM.html", "late_gilde_CSC_C.html", "late_gilde_SD_B.html", "late_gilde_TI.html",
                      "late_kennis_BIM.html", "late_kennis_CSC_C.html", "late_kennis_SD_B.html", "late_kennis_TI.html",
                      "late_team_BW.html", "late_team_DD.html", "late_team_HVG.html", "late_team_KE.html",
                      "late_team_RH.html"]
    else:
        file_names = ["index.html"]
    for file_name in file_names:
        shutil.copyfile(instances.get_html_path() + file_name, start.target_path + file_name)
    shutil.copytree(instances.get_html_path() + "plotly", start.target_path + "plotly", copy_function=shutil.copy2,
                    ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)

    if len(start.target_slb_path) > 0:
        slb_file_names = ["index.html", "index_slb.html"]
        print("Copy files to OneDrive slb")
        for file_name in slb_file_names:
            shutil.copyfile(instances.get_html_path() + file_name, start.target_slb_path + file_name)
        shutil.copytree(instances.get_html_path() + "plotly", start.target_slb_path + "plotly",
                        copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                        dirs_exist_ok=True)
    print("Done")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

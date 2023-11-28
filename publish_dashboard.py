import shutil

from lib.file import html_path, course_instance, inno_courses, read_start

start = read_start()
print("Copy files to OneDrive docenten")
if course_instance in inno_courses:
    file_names = ["index.html", "late.html",
              "late_gilde_BIM.html", "late_gilde_CSC_C.html", "late_gilde_SD_B.html", "late_gilde_TI.html",
              "late_kennis_BIM.html", "late_kennis_CSC_C.html", "late_kennis_SD_B.html", "late_kennis_TI.html",
              "late_team_BW.html", "late_team_DD.html", "late_team_HVG.html", "late_team_KE.html", "late_team_RH.html"]
else:
    file_names = ["index.html"]
for file_name in file_names:
    shutil.copyfile(html_path+file_name, start.target_path+file_name)
shutil.copytree(html_path +"plotly", start.target_path +"plotly", copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                dirs_exist_ok=True)

if len(start.target_slb_path) > 0:
    slb_file_names = ["index.html", "index_slb.html"]
    print("Copy files to OneDrive slb")
    for file_name in slb_file_names:
        shutil.copyfile(html_path+file_name, start.target_slb_path+file_name)
    shutil.copytree(html_path +"plotly", start.target_slb_path +"plotly", copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)
print("Done")
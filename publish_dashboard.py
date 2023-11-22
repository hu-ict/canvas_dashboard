import shutil

from lib.file import html_path, target_path, target_slb_path, tennant

print("Copy files to OneDrive docenten")

if tennant == "inno":
    file_names = ["index.html", "late.html",
              "late_gilde_BIM.html", "late_gilde_CSC_C.html", "late_gilde_SD_B.html", "late_gilde_TI.html",
              "late_kennis_BIM.html", "late_kennis_CSC_C.html", "late_kennis_SD_B.html", "late_kennis_TI.html",
              "late_team_BW.html", "late_team_DD.html", "late_team_HVG.html", "late_team_KE.html", "late_team_RH.html"]
else:
    file_names = ["index.html"]

for file_name in file_names:
    shutil.copyfile(html_path+file_name, target_path+file_name)
shutil.copytree(html_path +"plotly", target_path +"plotly", copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                dirs_exist_ok=True)
slb_file_names = ["index.html", "index_slb.html"]
if target_slb_path:
    print("Copy files to OneDrive slb")
    for file_name in slb_file_names:
        shutil.copyfile(html_path+file_name, target_slb_path+file_name)
    shutil.copytree(html_path +"plotly", target_slb_path +"plotly", copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)
print("Done")
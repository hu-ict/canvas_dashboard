import json
import os
import shutil

from lib.file import read_course_instance, ENVIRONMENT_FILE_NAME
from lib.lib_date import get_date_time_obj
from model.Role import Role
from model.Start import Start
from model.instance.Instance import Instance
from model.perspective.LevelMoments import LevelMoments
from model.perspective.Perspective import Perspective

instances = read_course_instance()
new_instance = input("Create new instance by giving name: ")
if instances.is_instance(new_instance):
    print("Instance already exists", new_instance)
    exit()

for category in instances.course_categories.keys():
    print(category)
category = input("Choose an instance category: ")
while category not in instances.course_categories.keys():
    print("Category doesn't exist", category)
    category = input("Choose an instance category: ")
print("Creating new course instance", new_instance)

instances.current_instance = new_instance
instances.course_categories[category].course_instances.append(new_instance)
print("Instance:", instances.current_instance)
project_path = instances.get_project_path()

course_instance = instances.current_instance
instance = Instance(course_instance, category)
instance.new_instance()
instances.instances[instance.name] = instance

start_file_name = instances.get_start_file_name()

canvas_course_id = input("Canvas course_id: ")


start = Start(canvas_course_id, "Project Groups", "", get_date_time_obj("2024-09-02T00:00:00Z"), get_date_time_obj("2025-01-31T23:59:59Z"),
              project_path + "templates//", "onedrive", "onedrive",
              project_path + "config_" + course_instance + ".json",
              project_path + "course_" + course_instance + ".json",
              project_path + "result_" + course_instance + ".json",
              project_path + "progress_" + course_instance + ".json",
              project_path + "workload_" + course_instance + ".json",
              project_path + "attendance_report.csv",
              "", "progress", "grade")
start.level_moments = LevelMoments("level_moments", "Peilmomenten", "progress", [])
perspective = Perspective("project", "Project", "samen", True, False)
start.perspectives[perspective.name] = perspective
role = Role("role", "Student", "border-dark")
start.roles.append(role)

os.makedirs(os.path.dirname(project_path), exist_ok=True)
os.makedirs(os.path.dirname(project_path +"dashboard_" + course_instance + "//"), exist_ok=True)
os.makedirs(os.path.dirname(project_path +"dashboard_" + course_instance + "//plotly//"), exist_ok=True)
os.makedirs(os.path.dirname(project_path+"templates//"), exist_ok=True)
os.makedirs(os.path.dirname(project_path+"test//"), exist_ok=True)

dir_names = ["css", "js", "scss", "vendor"]
for dir_name in dir_names:
    # shutil.copyfile(html_path+file_name, target_path+file_name)
    shutil.copytree(".//dashboard - lokaal//" + dir_name, project_path +"dashboard_" + course_instance + "//" + dir_name, copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                    dirs_exist_ok=True)

shutil.copytree(".//templates//", start.template_path, copy_function=shutil.copy2, ignore_dangling_symlinks=False, dirs_exist_ok=True)

with open(start_file_name, 'w') as f:
    dict_result = start.to_json([])
    json.dump(dict_result, f, indent=2)

with open(ENVIRONMENT_FILE_NAME, 'w') as f:
    dict_result = instances.to_json()
    json.dump(dict_result, f, indent=2)

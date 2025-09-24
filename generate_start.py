import json
import os
from lib.file import ENVIRONMENT_FILE_NAME, read_course_instances
from lib.lib_date import get_date_time_obj
from model.Start import Start
from model.instance.Instance import Instance

instances = read_course_instances()
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

course_instance = instances.current_instance
instance = Instance(course_instance, category)
instance.new_instance()
instances.instances[instance.name] = instance

start_file_name = instance.get_start_file_name()

canvas_course_id = input("Canvas course_id: ")
canvas_api_key = input("Canvas API-key: ")
if instance.is_instance_of("prop_courses"):
    attendance_path = instance.get_project_path() + "attendance_report.csv"
    project_group_name = "SECTIONS"
    guild_group_name = ""
else:
    attendance_path = None
    project_group_name = "Project Groups"
    guild_group_name = "Guild Groups"
start = Start(canvas_course_id,
              project_group_name,
              guild_group_name,
              get_date_time_obj("2025-09-01T00:00:00Z"),
              get_date_time_obj("2026-01-30T23:59:59Z"),
              "onedrive",
              attendance_path,
              canvas_api_key)

os.makedirs(os.path.dirname(instance.get_project_path()), exist_ok=True)
os.makedirs(os.path.dirname(instance.get_temp_path()), exist_ok=True)
os.makedirs(os.path.dirname(instance.get_html_root_path()), exist_ok=True)
os.makedirs(os.path.dirname(instance.get_html_path()), exist_ok=True)
os.makedirs(os.path.dirname(instance.get_student_path()), exist_ok=True)

with open(start_file_name, 'w') as f:
    dict_result = start.to_json([])
    json.dump(dict_result, f, indent=2)

with open(ENVIRONMENT_FILE_NAME, 'w') as f:
    dict_result = instances.to_json()
    json.dump(dict_result, f, indent=2)

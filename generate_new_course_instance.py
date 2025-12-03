import json
import os
from lib.file import read_environment
from model.environment.CourseInstance import CourseInstance
from model.environment.Environment import Environment, ENVIRONMENT_FILE_NAME

periods = {
    "sep25": {"start_date": "2025-09-01T00:00:00Z", "end_date": "2026-01-30T23:59:59Z"},
    "feb26": {"start_date": "2026-02-09T00:00:00Z", "end_date": "2026-07-10T23:59:59Z"},
    "sep26": {"start_date": "2026-08-31T00:00:00Z", "end_date": "2027-01-29T23:59:59Z"},
}

environment = read_environment(ENVIRONMENT_FILE_NAME)

for course_code in environment.courses:
    print(course_code)
course_code = input("Choose a course_code: ")
while course_code not in environment.get_course_names():
    print("course_code doesn't exist", course_code)
    course_code = input("Choose an course_code: ")
print("GNC05 - Using course ", course_code)

course = environment.get_course_by_name(course_code)
course_instance_name = input("Create new course_instance by giving name: ")
while course.get_course_instance_by_name(course_instance_name) is not None:
    print("course_instance already exists", course_instance_name)
    course_instance_name = input("Create new course_instance by giving name: ")
print("GNC07 - Creating course_instance", course_instance_name)
canvas_course_id = input("Canvas course_id: ")
target_path = input("Target path, i.e. onedrive file path: ")
# project_group_name = input("Canvas project_group_name (may p='Project Groups' or s='SECTIONS'): ")
# if project_group_name == "p":
#     project_group_name = "Project Groups"
# elif project_group_name == "s":
#     project_group_name = "SECTIONS"
# guild_group_name = input("Canvas guild_group_name (may g='Guild Groups' or empty): ")
# if guild_group_name == "g":
#     guild_group_name = "Guild Groups"
attendance_file = input("Canvas attendance_report.csv (attendance_report.csv): ")
for periode in periods:
    print(periode)
period = input("Choose the education period for the course_instance: ")
while period not in periods:
    print("period doesn't exists", period)
    cperiod = input("Choose the education period for the course_instance: ")
print("GNC09 - Creating course_instance", course_instance_name)

course_instance = CourseInstance(course_instance_name, course_code, canvas_course_id, target_path, periods[period], "DEV")
course.course_instances.append(course_instance)

os.makedirs(os.path.dirname(course_instance.get_project_path()), exist_ok=True)
os.makedirs(os.path.dirname(course_instance.get_temp_path()), exist_ok=True)
os.makedirs(os.path.dirname(course_instance.get_html_index_path()), exist_ok=True)
os.makedirs(os.path.dirname(course_instance.get_html_general_path()), exist_ok=True)
os.makedirs(os.path.dirname(course_instance.get_html_student_path()), exist_ok=True)

environment.current_instance = {"course_name": course_code, "course_instance_name": course_instance_name}
with open(ENVIRONMENT_FILE_NAME, 'w') as f:
    dict_result = environment.to_json()
    json.dump(dict_result, f, indent=2)
print("CourseInstane is created", course_instance_name)
print("Environment is updated", environment.name)


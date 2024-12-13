import json
import os
from lib.file import ENVIRONMENT_FILE_NAME, read_course_instances
from lib.lib_date import get_date_time_obj
from model.Start import Start
from model.instance.Instance import Instance


def main():
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
    else:
        attendance_path = None
    start = Start(canvas_course_id,
                  "Project Groups",
                  get_date_time_obj("2024-09-02T00:00:00Z"),
                  get_date_time_obj("2025-01-31T23:59:59Z"),
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


def main_generate(new_instance, category, canvas_course_id, canvas_api_key):
    instances = read_course_instances()

    if instances.is_instance(new_instance):
        print("Instance already exists", new_instance)
        exit()
    if category not in instances.course_categories.keys():
        print("Category doesn't exist", category)
        exit(404)

    instances.current_instance = new_instance
    instances.course_categories[category].course_instances.append(new_instance)
    print("Instance:", instances.current_instance)
    project_path = instances.get_project_path(new_instance)

    course_instance = instances.current_instance
    instance = Instance(course_instance, category)
    instance.new_instance()
    instances.instances[instance.name] = instance

    start_file_name = instances.get_start_file_name()

    start = Start(canvas_course_id,
                  "Project Groups",
                  get_date_time_obj("2024-09-02T00:00:00Z"),
                  get_date_time_obj("2025-01-31T23:59:59Z"),
                  "onedrive",
                  project_path + "attendance_report.csv",
                  canvas_api_key)

    os.makedirs(os.path.dirname(project_path), exist_ok=True)
    os.makedirs(os.path.dirname(project_path + "dashboard_" + course_instance + "//"), exist_ok=True)
    os.makedirs(os.path.dirname(project_path + "dashboard_" + course_instance + "//general//"), exist_ok=True)
    os.makedirs(os.path.dirname(project_path + "dashboard_" + course_instance + "//students//"), exist_ok=True)

    with open(start_file_name, 'w') as f:
        dict_result = start.to_json([])
        json.dump(dict_result, f, indent=2)

    with open(ENVIRONMENT_FILE_NAME, 'w') as f:
        dict_result = instances.to_json()
        json.dump(dict_result, f, indent=2)


if __name__ == "__main__":
    main()

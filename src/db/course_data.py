import os
import json

def get_course_instance_name():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_courses = os.path.join(base_dir, '..', '..' ,'courses', 'course_instances.json')
    # read the JSON files
    with open(json_courses) as file:
        data = json.load(file)

    return data["current_instance"]

def get_students(course_instance_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, '..', '..', 'courses', course_instance_name, f"result_{course_instance_name}.json")
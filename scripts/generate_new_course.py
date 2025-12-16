import json
import os

from scripts.lib.file import read_environment
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME
from scripts.model.environment.Course import Course

environment = read_environment(ENVIRONMENT_FILE_NAME)
course_code = input("Give the course_code for the new course: ")
if course_code in environment.get_course_names():
    print("course_code already exists", course_code, environment.get_course_names())
    course_instance_name = input("Give the course_code for the new course: ")
print("Creating new course", course_code)
course = Course(course_code)
environment.courses.append(course)

os.makedirs(os.path.dirname(course.get_path()), exist_ok=True)

with open(ENVIRONMENT_FILE_NAME, 'w') as f:
    dict_result = environment.to_json()
    json.dump(dict_result, f, indent=2)
print("Course is created", ENVIRONMENT_FILE_NAME)

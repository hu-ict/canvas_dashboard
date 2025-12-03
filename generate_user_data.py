import json

from lib.file import read_start, read_course, read_environment, read_secret_api_key
from lib.lib_date import get_actual_date
import sys

import csv

from model.environment.Environment import ENVIRONMENT_FILE_NAME
from model.environment.SecretApiKey import SECRET_API_KEY_FILE_NAME


class UserDictAdapter:
    def __init__(self, a_course_id, a_course_name, a_instance_name, a_start_date, a_end_date, a_name, a_email, a_role):
        self.canvas_course_id = a_course_id
        self.course_name = a_course_name
        self.instance_name = a_instance_name
        self.start_date = a_start_date
        self.end_date = a_end_date
        self.name = a_name
        self.email = a_email
        self.role = a_role

    def to_dict(self):
        return {
            "canvas_course_id": self.canvas_course_id,
            "course_name": self.course_name,
            "instance_name": self.instance_name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "user_name": self.name,
            "user_email": self.email,
            "user_role": self.role
        }


def generate_user_data(course_code, instance_name):
    print("GUD01 - generate_user_data.py")
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    print("GUD02 - Instance:", course_instance.name)

    user_data = list()
    course = read_course(course_instance.get_course_file_name())
    for student in course.students:
        user = UserDictAdapter(course_instance.canvas_course_id, course_instance.course_code, course_instance.name, course_instance.period["start_date"], course_instance.period["end_date"], student.name, student.email, "STUDENT")
        user_data.append(user)
    for teachers in course.teachers:
        user = UserDictAdapter(course_instance.canvas_course_id, course_instance.course_code, course_instance.name, course_instance.period["start_date"], course_instance.period["end_date"], teachers.name, teachers.email, "TEACHER")
        user_data.append(user)

    with open("courses/user_data.csv", mode="w", newline="", encoding="utf-8") as bestand:
        veldnamen = ["canvas_course_id", "course_name", "instance_name", "start_date", "end_date", "user_name", "user_email", "user_role"]
        csv_file = csv.DictWriter(bestand, fieldnames=veldnamen)
        csv_file.writeheader()
        for user in user_data:
            csv_file.writerow(user.to_dict())

    print("GUD99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) > 1:
        generate_user_data(sys.argv[1], sys.argv[2])
    else:
        generate_user_data("", "")

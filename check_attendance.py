import csv

from scripts.lib.file import read_course, read_environment
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME

def read_attendancy_csv(a_filename):
    print('F001 - read_attendancy_csv:', a_filename)
    attendancy = []
    with open(a_filename, 'r') as file:
        file_list = file.readlines()
    for item in file_list:
        attendancy.append(item.strip())
    return attendancy

def main():
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    execution = environment.get_execution_by_name("env_2")
    attendancy = read_attendancy_csv("attendancy.txt")
    course_instance = environment.get_current_instance()
    print("RUN213 - Instance:", course_instance.name)
    course_instance.execution_source_path = execution.source_path
    course = read_course(course_instance.get_course_file_name())
    print(len(attendancy))
    for student in course.students:
        if student.email not in attendancy:
            print("NOT", student.email)

main()
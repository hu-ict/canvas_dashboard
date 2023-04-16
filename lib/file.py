import json

from model.CourseConfig import CourseConfig
from model.CourseConfigStart import CourseConfigStart
from model.Student import Student
from model.Submission import Submission

course_config_start_file = "course_config_start.json"

def read_course_config_start():
    with open(course_config_start_file, mode='r', encoding="utf-8") as file_config_start:
        data = json.load(file_config_start)
        course_config_start = CourseConfigStart.from_dict(data)
        return course_config_start

def read_course_config(file_name):
    with open(file_name, mode='r', encoding="utf-8") as file_config:
        data = json.load(file_config)
        course_config = CourseConfig.from_dict(data)
        return course_config

def read_late_json():
    f = open('late.json')
    late_list = []
    data = json.load(f)
    for late_json in data:
        late = Submission.from_dict(late_json)
        late_list.append(late)
    # Closing file
    f.close()
    return late_list

def read_student_json():
    f = open('student_results.json')
    students = []
    data = json.load(f)
    for student_json in data['students']:
        student = Student.from_dict(student_json)
        students.append(student)
    # Closing file
    f.close()
    return students
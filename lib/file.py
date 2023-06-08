import json

from model.Course import Course
from model.CourseConfig import CourseConfig
from model.CourseConfigStart import CourseConfigStart
from model.Student import Student
from model.Submission import Submission

start_file_name = "start.json"


def read_start():
    print("read_start", start_file_name)
    with open(start_file_name, mode='r', encoding="utf-8") as file_config_start:
        data = json.load(file_config_start)
        course_config_start = CourseConfigStart.from_dict(data)
        return course_config_start


def read_config(config_file_name):
    print("read_config", config_file_name)
    with open(config_file_name, mode='r', encoding="utf-8") as course_config_file:
        data = json.load(course_config_file)
        course_config = CourseConfig.from_dict(data)
        return course_config


def read_course(course_file_name):
    print("read_course", course_file_name)
    with open(course_file_name, mode='r', encoding="utf-8") as file_course:
        data = json.load(file_course)
        course = CourseConfig.from_dict(data)
        return course


def read_results(result_file_name):
    print("read_result", result_file_name)
    with open(result_file_name, mode='r', encoding="utf-8") as file_result:
        data = json.load(file_result)
        course = Course.from_dict(data)
        return course


# def read_late_json(late_file_name):
#     print("read_late", late_file_name)
#     f = open(late_file_name)
#     late_list = []
#     data = json.load(f)
#     for late_json in data:
#         late = Submission.from_dict(late_json)
#         late_list.append(late)
#     # Closing file
#     f.close()
#     return late_list
#
#
# def read_student_json():
#     f = open('results.json')
#     students = []
#     data = json.load(f)
#     for student_json in data['student_groups']:
#         student = Student.from_dict(student_json)
#         students.append(student)
#     # Closing file
#     f.close()
#     return students

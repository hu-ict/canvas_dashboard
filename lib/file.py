import json

from model.ProgressHistory import ProgressHistory
from model.Result import Result
from model.CourseConfig import CourseConfig
from model.CourseConfigStart import CourseConfigStart
from model.TeamsApi import TeamsApi
from model.perspective.Perspectives import Perspectives

start_file_name = "start.json"

def read_start():
    print("read_start", start_file_name)
    with open(start_file_name, mode='r', encoding="utf-8") as file_config_start:
        data = json.load(file_config_start)
        start = CourseConfigStart.from_dict(data)
        return start


def read_levels(labels_file_name):
    print("read_labels", labels_file_name)
    with open(labels_file_name, mode='r', encoding="utf-8") as file_labels:
        data = json.load(file_labels)
        labels = Perspectives.from_dict(data)
        return labels


def read_config(config_file_name):
    print("read_config", config_file_name)
    with open(config_file_name, mode='r', encoding="utf-8") as course_config_file:
        data = json.load(course_config_file)
        config = CourseConfig.from_dict(data)
        return config


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
        result = Result.from_dict(data)
        return result


def read_progress(progress_file_name):
    print("read_progress", progress_file_name)
    with open(progress_file_name, mode='r', encoding="utf-8") as file_progress:
        data = json.load(file_progress)
        progress = ProgressHistory.from_dict(data)
        return progress


def read_msteams_api(msteams_api_file_name):
    print("read msteams_api", msteams_api_file_name)
    with open(msteams_api_file_name, mode='r', encoding="utf-8") as file_msteams_api:
        data = json.load(file_msteams_api)
        result = TeamsApi.from_dict(data)
        return result

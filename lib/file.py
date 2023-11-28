import csv
import json
import os

from model.CourseInstances import CourseInstances
from model.ProgressHistory import ProgressHistory
from model.Result import Result
from model.CourseConfig import CourseConfig
from model.Start import Start
from model.Submission import Submission
from model.TeamsApi import TeamsApi
from model.perspective.LevelSeries import LevelSeries


def read_course_instance():
    print("read_start", "course_instances.json")
    with open("course_instances.json", mode='r', encoding="utf-8") as file_course_instances:
        data = json.load(file_course_instances)
        course_instances = CourseInstances.from_dict(data)
        return course_instances


def read_start(start_file_name):
    print("read_start", start_file_name)
    with open(start_file_name, mode='r', encoding="utf-8") as file_start:
        data = json.load(file_start)
        start = Start.from_dict(data)
        return start


def read_labels_colors(labels_file_name):
    print("read_labels", labels_file_name)
    with open(labels_file_name, mode='r', encoding="utf-8") as file_labels:
        data = json.load(file_labels)
        level_series = LevelSeries.from_dict(data)
        return level_series


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
    if os.path.isfile(progress_file_name):
        with open(progress_file_name, mode='r', encoding="utf-8") as file_progress:
            data = json.load(file_progress)
            progress_history = ProgressHistory.from_dict(data)
            return progress_history
    else:
        progress_history = ProgressHistory()
        with open(progress_file_name, 'w') as file_progress:
            dict_result = progress_history.to_json()
            json.dump(dict_result, file_progress, indent=2)
        return progress_history


def read_msteams_api(msteams_api_file_name):
    print("read msteams_api", msteams_api_file_name)
    with open(msteams_api_file_name, mode='r', encoding="utf-8") as file_msteams_api:
        data = json.load(file_msteams_api)
        result = TeamsApi.from_dict(data)
        return result

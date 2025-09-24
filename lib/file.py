import json
import os
from model.ProgressHistory import ProgressHistory
from model.Result import Result
from model.CourseConfig import CourseConfig
from model.Start import Start
from model.TeamsApi import TeamsApi
from model.workload.WorkloadHistory import WorkloadHistory
from model.dashboard.Dashboard import Dashboard
from model.dashboard.Subplot import Subplot
from model.instance.CourseInstances import CourseInstances
from model.dashboard.LevelSerieCollection import LevelSerieCollection

ENVIRONMENT_FILE_NAME = ".//courses//course_instances.json"


def read_course_instances():
    print("F001 - read_course_instances", ENVIRONMENT_FILE_NAME)
    if os.path.isfile(ENVIRONMENT_FILE_NAME):
        with open(ENVIRONMENT_FILE_NAME, mode='r', encoding="utf-8") as file_course_instances:
            data = json.load(file_course_instances)
            course_instances = CourseInstances.from_dict(data)
            return course_instances
    else:
        course_instances = CourseInstances("")
        course_instances.new_environment()
        return course_instances


def read_start(start_file_name):
    print("F002 - read_start", start_file_name)
    with open(start_file_name, mode='r', encoding="utf-8") as file_start:
        data = json.load(file_start)
        start = Start.from_dict(data)
        return start


def read_levels(levels_file_name):
    print("F003 - read_levels", levels_file_name)
    with open(levels_file_name, mode='r', encoding="utf-8") as file_labels:
        data = json.load(file_labels)
        level_serie_colection = LevelSerieCollection.from_dict(data)
        return level_serie_colection


def read_config(config_file_name):
    print("F004 - read_config", config_file_name)
    with open(config_file_name, mode='r', encoding="utf-8") as course_config_file:
        data = json.load(course_config_file)
        config = CourseConfig.from_dict(data)
        return config


def read_course(course_file_name):
    print("F005 - read_course", course_file_name)
    with open(course_file_name, mode='r', encoding="utf-8") as file_course:
        data = json.load(file_course)
        course = CourseConfig.from_dict(data)
        return course


def read_results(result_file_name):
    print("F006 - read_result", result_file_name)
    with open(result_file_name, mode='r', encoding="utf-8") as file_result:
        data = json.load(file_result)
        result = Result.from_dict(data)
        return result


def read_progress(progress_file_name):
    print("F007 - read_progress", progress_file_name)
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


def read_workload(workload_file_name):
    print("F008 - read_workload", workload_file_name)
    if os.path.isfile(workload_file_name):
        with open(workload_file_name, mode='r', encoding="utf-8") as file_workload:
            data = json.load(file_workload)
            workload_history = WorkloadHistory.from_dict(data)
            return workload_history
    else:
        workload_history = WorkloadHistory()
        with open(workload_file_name, 'w') as file_workload:
            dict_result = workload_history.to_json()
            json.dump(dict_result, file_workload, indent=2)
        return workload_history


def read_msteams_api(msteams_api_file_name):
    print("F009 - read msteams_api", msteams_api_file_name)
    with open(msteams_api_file_name, mode='r', encoding="utf-8") as file_msteams_api:
        data = json.load(file_msteams_api)
        result = TeamsApi.from_dict(data)
        return result

def read_file_list(file_list_file_name):
    print("F010 - read read_file_list", file_list_file_name)
    with open(file_list_file_name, mode='r', encoding="utf-8") as file_list_file:
        result = json.load(file_list_file)
        return result

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def read_config_from_canvas(canvas_course):
    print("F021 - read config_file from Canvas", "config-dot-json")
    page = canvas_course.get_page("config-dot-json")
    config_file = remove_html_tags(page.body)
    data = json.loads(config_file)
    return CourseConfig.from_dict(data)


def read_levels_from_canvas1(canvas_course):
    print("F022 - read levels_file from Canvas", "levels-dot-json")
    page = canvas_course.get_page("levels-dot-json")
    config_file = remove_html_tags(page.body)
    data = json.loads(config_file)
    level_series = LevelSerieCollection.from_dict(data)
    return level_series


def read_subplots_from_canvas1(canvas_course):
    print("F022 - read subplot_file from Canvas", "subplot-dot-json")
    page = canvas_course.get_page("subplot-dot-json")
    config_file = remove_html_tags(page.body)
    data = json.loads(config_file)
    subplot = Subplot.from_dict(data)
    return subplot

def read_dashboard_from_canvas(canvas_course):
    print("F023 - read dashboard_file from Canvas", "dashboard-dot-json")
    page = canvas_course.get_page("dashboard-dot-json")
    dashboard_file = remove_html_tags(page.body)
    data = json.loads(dashboard_file)
    dashboard = Dashboard.from_dict(data)
    return dashboard

def read_plotly(plotly_file_name):
    with open(plotly_file_name, mode='r', encoding="utf-8") as file_result:
        lines = file_result.readlines()
        result_str = ""
        for line in lines:
            result_str += line.strip()
        return result_str


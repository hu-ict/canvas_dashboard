import json
import os
from pathlib import Path

from scripts.model.ProgressHistory import ProgressHistory
from scripts.model.Result import Result
from scripts.model.CourseConfig import CourseConfig
from scripts.model.Start import Start
from scripts.model.TeamsApi import TeamsApi
from scripts.model.environment.Environment import Environment
from scripts.model.environment.SecretApiKey import SecretApiKey
from scripts.model.environment.Workflow import Workflow
from scripts.model.workload.WorkloadHistory import WorkloadHistory
from scripts.model.dashboard.Dashboard import Dashboard
from scripts.model.dashboard.Subplot import Subplot
from scripts.model.dashboard.LevelSerieCollection import LevelSerieCollection


def read_environment(file_name):
    print("F031 - read_environment", file_name)
    print("F032 - current path", os.getcwd())
    if os.path.isfile(file_name):
        with open(file_name, mode='r', encoding="utf-8") as environment_file:
            data = json.load(environment_file)
            environment = Environment.from_dict(data)
            return environment
    else:
        print("F034 - read_environment file not found", file_name)
    return None


def read_workflow(workflow_file_name):
    print("F032 - read_workflow", workflow_file_name)
    if os.path.isfile(workflow_file_name):
        with open(workflow_file_name, mode='r', encoding="utf-8") as workflow_file:
            data = json.load(workflow_file)
            environment = Workflow.from_dict(data)
            return environment
    return None


def read_secret_api_key(file_name):
    print("F033 - read_secret_api_key", file_name)
    if os.path.isfile(file_name):
        with open(file_name, mode='r', encoding="utf-8") as secret_api_key_file:
            data = json.load(secret_api_key_file)
            secret_api_key = SecretApiKey.from_dict(data)
            return secret_api_key
    else:
        print("F034 - read_secret_api_key file not found", file_name)
    return None

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


def read_course(course_file_name):
    print("F004 - current path", os.getcwd())
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


def write_results(result_file_name, results):
    with open(result_file_name, 'w', encoding='utf-8') as f:
        dict_result = results.to_json()
        json.dump(dict_result, f, indent=2, ensure_ascii=False)


def read_progress_history(progress_file_name):
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


def write_progress_history(progress_file_name, progress_history):
    with open(progress_file_name, 'w') as f:
        dict_result = progress_history.to_json()
        json.dump(dict_result, f, indent=2)


def write_course(file_name, course):    # Write JSON file with UTF-8 encoding
    with open(file_name, "w", encoding="utf-8") as file:
        dict_result = course.to_json()
        json.dump(dict_result, file, ensure_ascii=False, indent=2)


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
    course_config = CourseConfig.from_dict(data)
    return course_config


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
    print("F023 - Read dashboard_file from Canvas dashboard-dot-json", canvas_course.name)
    page = canvas_course.get_page("dashboard-dot-json")
    page = canvas_course.get_page("dashboard-dot-json")
    dashboard_file = remove_html_tags(page.body)
    data = json.loads(dashboard_file)
    dashboard = Dashboard.from_dict(data)
    return dashboard


def read_dashboard(dashboard_file_name):
    print("F024 - Read dashboard_file from os:", dashboard_file_name)
    with open(dashboard_file_name, mode='r', encoding="utf-8") as file_dashboard:
        data = json.load(file_dashboard)
        dashboard = Dashboard.from_dict(data)
        return dashboard


def read_plotly(plotly_file_name):
    with open(plotly_file_name, mode='r', encoding="utf-8") as file_result:
        lines = file_result.readlines()
        result_str = ""
        for line in lines:
            result_str += line.strip()
        return result_str


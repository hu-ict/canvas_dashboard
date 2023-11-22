import json
import os

from model.ProgressHistory import ProgressHistory
from model.Result import Result
from model.CourseConfig import CourseConfig
from model.CourseConfigStart import CourseConfigStart
from model.TeamsApi import TeamsApi
from model.perspective.LevelSeries import LevelSeries

tennant = "prop"

if tennant == "inno":
    start_file_name1 = "start_inno.json"
    plot_path = ".//dashboard - lokaal//plotly//"
    html_path = ".//dashboard - lokaal//"
    template_path = ".//templates_inno//"
    target_path = "C://Users//berend.wilkens//OneDrive - Stichting Hogeschool Utrecht//General//dashboard//"
    target_slb_path = "C://Users//berend.wilkens//Stichting Hogeschool Utrecht//INNO - SLB - General//INNO dashboard - SLB//"
elif tennant == "prop":
    start_file_name1 = "start_prop.json"
    plot_path = ".//dashboard - prop//plotly//"
    html_path = ".//dashboard - prop//"
    template_path = ".//templates_prop//"
    target_path = "C://Users//berend.wilkens//Stichting Hogeschool Utrecht//(EXT) Propedeuse blok A 2023-2024 (docenten) - General//dashboard - prop//"
    target_slb_path = None
else:
    start_file_name1 = "start_bims3.json"
    plot_path = ".//dashboard - bims3//plotly//"
    html_path = ".//dashboard - bims3//"

def read_start():
    print("read_start", start_file_name1)
    with open(start_file_name1, mode='r', encoding="utf-8") as file_config_start:
        data = json.load(file_config_start)
        start = CourseConfigStart.from_dict(data)
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

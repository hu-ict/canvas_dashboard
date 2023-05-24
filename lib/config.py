from datetime import datetime
import pytz

API_URL = "https://canvas.hu.nl/"
DATE_TIME_STR = '%Y-%m-%dT%H:%M:%SZ'
ALT_DATE_TIME_STR = '%Y-%m-%dT%H:%M:%S.%f%z'
timezone = pytz.timezone("Europe/Amsterdam")
actual_date = datetime.now()
NOT_GRADED = "Nog niet beoordeeld."
plot_path = "./dashboard - lokaal/plotly/"


group_id_dict = {
    "AI": 62149,
    "BIM": 62903,
    "CSC": 61719,
    "SD_B": 61367,
    "SD_F": 62609,
    "TI": 62138,
}

score_tabel = {0: "Geen voortgang", 1: "Onvoldoende voortgang", 2: "Voldoende voortgang", 3: "Goede voortgang"}

roles = {"AI": "AI",
         "BIM": "BIM",
         "CSC-B": "CSC",
         "CSC-C": "CSC",
         "SD-C-Back-End": "SD_B",
         "SD-D-Front-End": "SD_F",
         "SD-AB-Back-End-Verlenger": "SD_B",
         "TI": "TI",
         "Innovation 1": "INNO"
         }


def get_role(name):
    if roles.get(name):
        return roles[name]
    else:
        return ""


def get_date_time_obj(date_time_str):
    date_time_obj = datetime.strptime(date_time_str, DATE_TIME_STR)
    date_time_obj = date_time_obj.astimezone(timezone)
    return date_time_obj


def get_date_time_str(date_time):
    date_time_str = date_time.strftime(DATE_TIME_STR)
    return date_time_str


def date_to_day(start_date, actual_date):
    if actual_date:
        return (actual_date - start_date).days
    return 1

# def str_date_to_day(actual_date_str):
#     if actual_date_str:
#         actual_date = datetime.strptime(actual_date_str, DATE_TIME_STR)
#     else:
#         actual_date = datetime.strptime("2023-02-14", '%Y-%m-%d')
#     return (actual_date - start_date).days

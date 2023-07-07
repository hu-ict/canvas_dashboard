from datetime import datetime
import pytz

API_URL = "https://canvas.hu.nl/"
DATE_TIME_STR = '%Y-%m-%dT%H:%M:%SZ'
DATE_TIME_LOC = '%d-%m-%Y'
ALT_DATE_TIME_STR = '%Y-%m-%dT%H:%M:%S.%f%z'
timezone = pytz.timezone("Europe/Amsterdam")
actual_date = datetime.now()
NOT_GRADED = "Nog niet beoordeeld."
plot_path = "./dashboard - lokaal/plotly/"
template_path = "./dashboard - lokaal/"

group_id_dict = {
    "AI": 62149,
    "BIM": 62903,
    "CSC": 61719,
    "SD_B": 61367,
    "SD_F": 62609,
    "TI": 62138,
}

peil_labels = ["Halfweg", "Sprint 7", "Beoordeling"]

hover_style=dict(
        bgcolor="white",
        font_size=16,
        font_family="Helvetica"
)

colors_bar = {
    'Leeg': '#666666',
    'Geen': '#f25829',
    'Onvoldoende': '#f2a529',
    'Voldoende': '#85e043',
    'Goede': '#2bad4e'
}

score_tabel_team = {
    0: "Niet zichtbaar",
    1: "Startend",
    2: "Samenwerkend",
    3: "Excellerend"
}

score_tabel = {
    -9: "Puntenaftrek",
    -8: "Puntenaftrek",
    -7: "Puntenaftrek",
    -6: "Puntenaftrek",
    -5: "Puntenaftrek",
    -4: "Puntenaftrek",
    -3: "Puntenaftrek",
    -2: "Puntenaftrek",
    -1: "Puntenaftrek",
    0: "Geen",
    1: "In ontwikkeling",
    2: "Op niveau",
    3: "Boven niveau"}

voortgang_tabel = {
    -1: "Onbekend",
    0: "Geen voortgang",
    1: "Onvoldoende voortgang",
    2: "Voldoende voortgang",
    3: "Goede voortgang"}

beoordeling_tabel = {
    -1: "Onbekend",
    0: "Niet aanwezig",
    1: "Nog niet op niveau",
    2: "Op niveau",
    3: "Boven niveau"}

color_tabel = {
    -1: '#aaaaaa',
    0: '#f25829',
    1: '#f2a529',
    2: '#85e043',
    3: '#2bad4e',
    4: "#666666"
}

def get_marker_size(graded):
    if graded:
        return 12
    else:
        return 6


def get_date_time_obj(date_time_str):
    date_time_obj = datetime.strptime(date_time_str, DATE_TIME_STR)
    date_time_obj = date_time_obj.astimezone(timezone)
    return date_time_obj


def get_date_time_str(a_date_time_str):
    date_time_str = a_date_time_str.strftime(DATE_TIME_STR)
    return date_time_str


def get_date_time_loc(a_date_time_obj):
    date_time_str = a_date_time_obj.strftime(DATE_TIME_LOC)
    return date_time_str


def date_to_day(a_start_date, a_actual_date):
    if a_actual_date:
        return (a_actual_date - a_start_date).days
    return 1

# def str_date_to_day(actual_date_str):
#     if actual_date_str:
#         actual_date = datetime.strptime(actual_date_str, DATE_TIME_STR)
#     else:
#         actual_date = datetime.strptime("2023-02-14", '%Y-%m-%d')
#     return (actual_date - start_date).days

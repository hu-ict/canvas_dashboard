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
template_path_general = "./dashboard - lokaal/"
template_path_slb = "./dashboard - slb/"

peil_labels = ["Sprint 4", "Sprint 7", "Beoordeling"]
peil_levels = [-1, 0, 1, 2, 3]

hover_style=dict(
        bgcolor="#eeeeee",
        font_size=16,
        font_family="Helvetica"
)

score_dict = {
    -2:{'niveau': 'Leeg', 'voortgang': 'Nog niet bepaald', 'beoordeling': 'Nog niet beoordeeld', 'color': 'cornflowerblue'},
    -1:{'niveau': 'Leeg', 'voortgang': 'Leeg', 'beoordeling': 'Onbekend', 'color': '#cccccc'},
    0: {'niveau': 'Niet zichtbaar', 'voortgang': 'Geen voortgang', 'beoordeling': 'Niet aanwezig', 'color': '#f25829'},
    1: {'niveau': 'Startend', 'voortgang': 'Onvoldoende voortgang', 'beoordeling': 'Onder niveau', 'color': '#f2a529'},
    2: {'niveau': 'Samenwerkend', 'voortgang': 'Voldoende voortgang', 'beoordeling': 'Op niveau', 'color': '#85e043'},
    3: {'niveau': 'Excellerend', 'voortgang': 'Goede voortgang', 'beoordeling': 'Boven niveau', 'color': '#2bad4e'}
}

colors_bar = {score_dict[-1]['voortgang']:score_dict[-1]['color'],
              score_dict[0]['voortgang']:score_dict[0]['color'],
              score_dict[1]['voortgang']:score_dict[1]['color'],
              score_dict[2]['voortgang']:score_dict[2]['color'],
              score_dict[3]['voortgang']:score_dict[3]['color']}


def fraction_to_level(a_fraction):
    if a_fraction < 0.01:
        return score_dict[0]
    elif a_fraction < 0.55:
        return score_dict[1]
    elif a_fraction < 0.80:
        return score_dict[2]
    else:
        return score_dict[3]

def get_marker_size(graded):
    if graded:
        return 14
    else:
        return 9


def get_date_time_obj(date_time_str):
    date_time_obj = datetime.strptime(date_time_str, DATE_TIME_STR)
    date_time_obj = date_time_obj.astimezone(timezone)
    return date_time_obj


def get_date_time_str(a_date_time_obj):
    date_time_str = a_date_time_obj.strftime(DATE_TIME_STR)
    return date_time_str


def get_date_time_loc(a_date_time_obj):
    date_time_str = a_date_time_obj.strftime(DATE_TIME_LOC)
    return date_time_str


def date_to_day(a_start_date, a_actual_date):
    if a_actual_date:
        return (a_actual_date - a_start_date).days
    return 1

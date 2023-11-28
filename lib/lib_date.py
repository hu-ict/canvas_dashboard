from datetime import datetime
import pytz

API_URL = "https://canvas.hu.nl/"
DATE_TIME_STR = '%Y-%m-%dT%H:%M:%SZ'
DATE_TIME_LOC = '%d-%m-%Y'
ALT_DATE_TIME_STR = '%Y-%m-%dT%H:%M:%S.%f%z'
timezone = pytz.timezone("Europe/Amsterdam")


def get_date_time_obj(date_time_str):
    if len(date_time_str) == 0:
        return None
    date_time_obj = datetime.strptime(date_time_str, DATE_TIME_STR)
    date_time_obj = date_time_obj.astimezone(timezone)
    return date_time_obj

def get_date_time_obj_loc(date_time_str):
    if len(date_time_str) == 0:
        return None
    date_time_obj = datetime.strptime(date_time_str, DATE_TIME_LOC)
    date_time_obj = date_time_obj.astimezone(timezone)
    return date_time_obj

def get_date_time_str(a_date_time_obj):
    if not a_date_time_obj:
        return ""
    date_time_str = a_date_time_obj.strftime(DATE_TIME_STR)
    return date_time_str


def get_date_time_loc(a_date_time_obj):
    date_time_str = a_date_time_obj.strftime(DATE_TIME_LOC)
    return date_time_str


def date_to_day(a_start_date, a_actual_date):
    if a_actual_date:
        return (a_actual_date - a_start_date).days
    return 1


def get_assignment_date(due_at, lock_at, end_date):
    if due_at:
        return get_date_time_obj(due_at)
    if lock_at:
        return get_date_time_obj(lock_at)
    return end_date


def get_actual_date():
    return get_date_time_obj(get_date_time_str(datetime.now()))

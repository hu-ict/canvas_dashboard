import numpy as np
from scipy.interpolate import interp1d
from model.Bandwidth import Bandwidth, Point
import plotly.express as px
import plotly.graph_objs as go


def calc_dev(iterations, r, a, b, c):
    iteration_list = []
    for x in range(iterations-r+1):
        y = a*x*x+b*x+c
        if y < 0:
            y = 0
        iteration_list.append(y)
    for x in range(r):
        iteration_list.append(y)
    return iteration_list


def calc_interp(x1, y1, x2, y2, x):
    return (y2-y1)/(x2-x1)*x


def find_between(serie, x):
    max_day = max(serie)
    if x > serie[max_day]['day']:
        #de dag is later dan de laatste dag
        return serie[max_day]["day"], serie[max_day]["sum"], x, serie[max_day]["sum"]
    last_day = 0
    for day in serie:
        if serie[last_day]["day"] <= x <= serie[day]["day"]:
            return serie[last_day]["day"], serie[last_day]["sum"], serie[day]["day"], serie[day]["sum"]
        last_day = day


def bandwidth_builder(assignment_group, a_days_in_semester):
    points = []
    x_reparatie_periode = 14
    y_start = assignment_group.total_points/35
    x_time = calc_dev(a_days_in_semester, 0, 0, 1, 0)
    # bereken bandbreedte
    if assignment_group.strategy == "EXPONENTIAL":
        band_lower = calc_dev(a_days_in_semester, x_reparatie_periode, 0.00161, 0.1, 0)
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0.00223, 0.1, y_start*4)
    elif assignment_group.name == "CSC - Cloud":
        b = (assignment_group.lower_points + y_start + 18) / (a_days_in_semester - x_reparatie_periode)
        band_lower = calc_dev(a_days_in_semester, x_reparatie_periode, 0, b, - y_start - 18)
        b = (assignment_group.upper_points - y_start) / (a_days_in_semester - x_reparatie_periode)
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0, b, y_start)
    elif assignment_group.strategy == "CONSTANT":
        # propedeuse perspectieven
        c = assignment_group.lower_points
        band_lower = calc_dev(a_days_in_semester, x_reparatie_periode, 0, 0, c)
        c = assignment_group.upper_points
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0, 0, c)
    elif assignment_group.strategy == "ATTENDANCE":
        # propedeuse perspectieven
        c = assignment_group.lower_points
        band_lower = calc_dev(a_days_in_semester, x_reparatie_periode, 0, 0, c)
        c = assignment_group.upper_points
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0, 0, c)
    elif assignment_group.strategy == "POINTS":
        serie = {0: {"day": 0, "sum": 0}}
        total_points = 0
        y = 0
        lower_fraction = assignment_group.lower_points/assignment_group.total_points
        upper_fraction = assignment_group.upper_points/assignment_group.total_points
        for assignment in assignment_group.assignments:
            total_points += assignment.points
            serie[assignment.assignment_day] = {"day": assignment.assignment_day, "sum": total_points}
        band_lower = []
        band_upper = []
        for x in x_time:
            x1, y1, x2, y2 = find_between(serie, x)
            if (x2-x1) != 0:
                y = calc_interp(x1, y1, x2, y2, x-x1)+y1
            band_lower.append(y * lower_fraction)
            band_upper.append(y * upper_fraction)
    elif assignment_group.strategy == "FIXED":
        serie = {0: {"day": 0, "sum": 0}}
        total_points = 0
        y = 0
        lower_fraction = assignment_group.lower_points/assignment_group.total_points
        for assignment in assignment_group.assignments:
            total_points += assignment.points
            serie[assignment.assignment_day] = {"day": assignment.assignment_day+7, "sum": total_points}
        print(serie.items())
        band_lower = []
        band_upper = []
        for x in x_time:
            x1, y1, x2, y2 = find_between(serie, x)
            band_lower.append(y1)
            band_upper.append(assignment_group.upper_points)

    else:
        #assignment_group.strategy == "LINEAIR"
        b = (assignment_group.lower_points + y_start) / (a_days_in_semester - x_reparatie_periode)
        band_lower = calc_dev(a_days_in_semester, x_reparatie_periode, 0, b, -y_start)
        b = (assignment_group.upper_points - y_start) / (a_days_in_semester - x_reparatie_periode)
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0, b, y_start)

    print(len(x_time), len(band_lower), len(band_upper))
    for i in range(len(x_time)):
        if i < len(band_lower):
            points.append(Point(x_time[i], band_lower[i], band_upper[i]))
    new = Bandwidth()
    new.days = x_time
    new.lowers = band_lower
    new.uppers = band_upper
    new.points = points
    return new

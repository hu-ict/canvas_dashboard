import json

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


def find_between(serie, level, x):
    max_day = max(serie)
    if x > serie[max_day]['day']:
        #de dag is later dan de laatste dag
        return serie[max_day]["day"], serie[max_day][level], x, serie[max_day][level]
    last_day = 0
    for day in serie:
        if serie[last_day]["day"] <= x <= serie[day]["day"]:
            return serie[last_day]["day"], serie[last_day][level], serie[day]["day"], serie[day][level]
        last_day = day


def bandwidth_builder(assignment_group, days_in_semester):
    points = []
    x_reparatie_periode = 14
    y_start = assignment_group.upper_points/25
    x_time = calc_dev(days_in_semester, 0, 0, 1, 0)
    # bereken bandbreedte
    if assignment_group.strategy == "EXPONENTIAL":
        lower_a = assignment_group.lower_points / (days_in_semester-x_reparatie_periode) / (days_in_semester-x_reparatie_periode)
        upper_a = (assignment_group.upper_points - y_start*3) / (days_in_semester-x_reparatie_periode) / (days_in_semester-x_reparatie_periode)
        band_lower = calc_dev(days_in_semester, x_reparatie_periode, lower_a, 0.00, 0)
        band_upper = calc_dev(days_in_semester, x_reparatie_periode, upper_a, 0.00, y_start*3)
    elif assignment_group.strategy == "LIN_POINTS":
        lower_a = 0
        upper_a = 0
        lower_b = assignment_group.lower_points / assignment_group.total_points
        upper_b = assignment_group.upper_points / assignment_group.total_points
        lower_c = 0
        upper_c = 0
        serie = {0: {"day": 0, "sum": 0}}
        total_points = 0
        y = 0
        print(
            f"LB02 - lower_points {assignment_group.lower_points} upper_points {assignment_group.upper_points} total_points {assignment_group.total_points}")
        print(f"LB03 - lower a {lower_a:5} b {lower_b:5.3} c {lower_c:5}")
        print(f"LB04 - upper a {upper_a:5} b {upper_b:5.3} c {upper_c:5}")
        total_points = 0
        for assignment in assignment_group.assignments:
            total_points += assignment.points
            serie[assignment.assignment_day] = {"day": assignment.assignment_day, "sum": total_points}
            output = f"LB08 - Day points; {assignment.points:3};{assignment.assignment_day:4};{total_points:>4}"
            output = output.replace('.', ',')
            print(output)
        band_lower = []
        band_upper = []
        for x in x_time:
            x1, y1, x2, y2 = find_between(serie, "sum", x)
            if (x2-x1) != 0:
                y = calc_interp(x1, y1, x2, y2, x-x1)+y1
            band_lower.append(y * lower_b)
            band_upper.append(y * upper_b)
    elif assignment_group.strategy == "EXP_POINTS":
        print("LB61 -", assignment_group)
        const = 7
        lower_c = float(assignment_group.lower_c)
        lower_b = 1 / const
        lower_a = (assignment_group.lower_points - lower_c - assignment_group.total_points / const) / (assignment_group.total_points * assignment_group.total_points)
        upper_c = float(assignment_group.upper_c)
        upper_b = 1 / const
        upper_a = (assignment_group.upper_points - upper_c - assignment_group.total_points / const) / (assignment_group.total_points * assignment_group.total_points)
        print(f"LB62 - lower_points {assignment_group.lower_points} upper_points {assignment_group.upper_points} total_points {assignment_group.total_points}")
        print(f"LB63 - lower a {lower_a:8.5} b {lower_b:5.2} c {lower_c:5.2}")
        print(f"LB64 - upper a {upper_a:8.5} b {upper_b:5.2} c {upper_c:5.2}")
        serie = {0: {"day": 0, "value_day": 0, "lower": 0, "upper": int(assignment_group.total_points/30)}}
        total_points = 0
        lower_y = lower_c
        upper_y = upper_c
        output = f"LB66 - Day points;  0;  0;  0;{lower_y:5.2f};{upper_y:5.2f}"
        output = output.replace('.', ',')
        print(output)
        # print(assignment.assignment_day, assignment.points, "value_day", total_points, "lower =", lower_y, "upper =", upper_y)
        serie[0] = {"day": 0, "value_day": 0, "lower": lower_y, "upper": upper_y}
        for assignment in assignment_group.assignments:
            total_points += assignment.points
            lower_y = lower_a * total_points * total_points + lower_b * total_points + lower_c
            upper_y = upper_a * total_points * total_points + upper_b * total_points + upper_c
            output = f"LB68 - Day points; {assignment.points:2};{assignment.assignment_day:3};{total_points:>3};{lower_y:5.2f};{upper_y:5.2f}"
            output = output.replace('.',',')
            print(output)
            # print(assignment.assignment_day, assignment.points, "value_day", total_points, "lower =", lower_y, "upper =", upper_y)
            serie[assignment.assignment_day] = {"day": assignment.assignment_day, "value_day": total_points, "lower": lower_y, "upper": upper_y}
        band_lower = []
        band_upper = []
        for x in x_time:
            x1, y1, x2, y2 = find_between(serie, "lower", x)
            if (x2-x1) != 0:
                y = calc_interp(x1, y1, x2, y2, x-x1)+y1
            else:
                y = y2
            band_lower.append(y)
        for x in x_time:
            x1, y1, x2, y2 = find_between(serie, "upper", x)
            if (x2-x1) != 0:
                y = calc_interp(x1, y1, x2, y2, x-x1)+y1
            else:
                y = y2
            band_upper.append(y)
        with open("series_"+str(assignment_group.id)+".json", 'w') as f:
            dict_result = serie
            json.dump(dict_result, f, indent=2)
    elif assignment_group.strategy == "CONSTANT":
        # propedeuse perspectieven
        c = assignment_group.lower_points
        band_lower = calc_dev(days_in_semester, x_reparatie_periode, 0, 0, c)
        c = assignment_group.upper_points
        band_upper = calc_dev(days_in_semester, x_reparatie_periode, 0, 0, c)
    elif assignment_group.strategy == "ATTENDANCE":
        # propedeuse perspectieven
        c = assignment_group.lower_points
        band_lower = calc_dev(days_in_semester, x_reparatie_periode, 0, 0, c)
        c = assignment_group.upper_points
        band_upper = calc_dev(days_in_semester, x_reparatie_periode, 0, 0, c)
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
            x1, y1, x2, y2 = find_between(serie, "sum", x)
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
        b = (assignment_group.lower_points + y_start) / (days_in_semester - x_reparatie_periode)
        band_lower = calc_dev(days_in_semester, x_reparatie_periode, 0, b, -y_start)
        b = (assignment_group.upper_points - y_start) / (days_in_semester - x_reparatie_periode)
        band_upper = calc_dev(days_in_semester, x_reparatie_periode, 0, b, y_start)
    for i in range(len(x_time)):
        if i < len(band_lower):
            points.append(Point(x_time[i], band_lower[i], band_upper[i]))
    new = Bandwidth()
    new.days = x_time
    new.lowers = band_lower
    new.uppers = band_upper
    new.points = points

    return new

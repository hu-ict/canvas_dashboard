from model.Bandwidth import Bandwidth, Point


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

def bandwidth_builder(assignment_group, a_days_in_semester):
    points = []
    x_reparatie_periode = 14
    y_start = assignment_group.total_points/35
    x_time = calc_dev(a_days_in_semester, 0, 0, 1, 0)
    # bereken bandbreedte
    if assignment_group.name == "TEAM":
        band_lower = calc_dev(a_days_in_semester, x_reparatie_periode, 0.00161, 0.1, 0)
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0.00223, 0.1, y_start*4)
    elif assignment_group.name == "CSC - Cloud" or assignment_group.name == "SD-Backend":
        b = (assignment_group.lower_points + y_start + 18) / (a_days_in_semester - x_reparatie_periode)
        band_lower = calc_dev(a_days_in_semester, x_reparatie_periode, 0, b, - y_start - 18)
        b = (assignment_group.upper_points - y_start) / (a_days_in_semester - x_reparatie_periode)
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0, b, y_start)
    elif assignment_group.id == 69428 or assignment_group.id == 71093 or assignment_group.id == 69429:
        # propedeuse perspectieven
        c = assignment_group.lower_points
        band_lower = calc_dev(a_days_in_semester, x_reparatie_periode, 0, 0, c)
        c = assignment_group.upper_points
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0, 0, c)
    elif assignment_group.name == "TI - Embedded":
        raw_serie = []
        total_points = 0
        last_day = 0
        for assignment in assignment_group.assignments:
            total_points += assignment.points
            raw_serie.append({"day": assignment.assignment_day-last_day, "sum": total_points})
            last_day = assignment.assignment_day
        band_lower = []
        c = 0
        lower_percentage = 0.55
        for raw in raw_serie:
            print(raw)
            if raw["day"] == 0:
                pass
            else:
                b = raw["sum"]*lower_percentage/raw["day"]
                band_lower += calc_dev(raw["day"], 0, 0, b, c)
                c = raw["sum"]*lower_percentage
            print(band_lower)

        b = (assignment_group.upper_points - y_start) / (a_days_in_semester - x_reparatie_periode)
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0, b, y_start)

    else:
        b = (assignment_group.lower_points + y_start) / (a_days_in_semester - x_reparatie_periode)
        band_lower = calc_dev(a_days_in_semester, x_reparatie_periode, 0, b, -y_start)
        b = (assignment_group.upper_points - y_start) / (a_days_in_semester - x_reparatie_periode)
        band_upper = calc_dev(a_days_in_semester, x_reparatie_periode, 0, b, y_start)

    for i in range(len(x_time)):
        points.append(Point(x_time[i], band_lower[i], band_upper[i]))
    new = Bandwidth()
    new.days = x_time
    new.lowers = band_lower
    new.uppers = band_upper
    new.points = points
    return new

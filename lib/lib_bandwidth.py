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
from model.Bandwidth import Bandwidth
from model.perspective.AttendanceMoment import AttendanceMoment
from model.perspective.Policy import Policy


class Attendance:
    def __init__(self, name, title, levels, show_points, show_flow, strategy, total_points, lower_points, upper_points, bandwidth, policy):
        self.name = name
        self.title = title
        self.levels = levels
        self.show_points = show_points
        self.show_flow = show_flow
        self.strategy = strategy
        self.total_points = total_points
        self.lower_points = lower_points
        self.upper_points = upper_points
        self.bandwidth = bandwidth
        self.policy = policy
        self.attendance_moments = []

    def to_json(self):
        check = lambda x: self.bandwidth.to_json() if x is not None else None
        dict_result = {
            'name': self.name,
            'title': self.title,
            'levels': self.levels,
            'show_points': self.show_points,
            'show_flow': self.show_flow,
            'strategy': self.strategy,
            'total_points': self.total_points,
            'lower_points': self.lower_points,
            'upper_points': self.upper_points,
            'policy': self.policy.to_json(),
            'attendance_moments': list(map(lambda m: m.to_json(), self.attendance_moments))

        }
        if self.bandwidth is not None:
            dict_result['bandwidth'] = self.bandwidth.to_json()
        else:
            dict_result['bandwidth'] = None
        return dict_result

    def __str__(self):
        return f'Attendance({self.name}, {self.title}, {self.attendance_moments}, {self.levels}, , {self.policy})'

    def get_moment(self, day):
        for moment in self.attendance_moments:
            if moment.attendance_day == day:
                return moment
        else:
            None

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        if 'policy' in data_dict.keys():
            policy = Policy.from_dict(data_dict['policy'])
        else:
            policy = None
        if 'bandwidth' in data_dict.keys():
            bandwidth = Bandwidth.from_dict(data_dict['bandwidth'])
        else:
            bandwidth = None

        new = Attendance(data_dict['name'], data_dict['title'], data_dict['levels'], data_dict['show_points'], data_dict['show_flow'],
                         data_dict['strategy'], data_dict['total_points'], data_dict['lower_points'], data_dict['upper_points'], bandwidth, policy)
        if 'attendance_moments' in data_dict.keys():
            new.attendance_moments = list(map(lambda s: AttendanceMoment.from_dict(s), data_dict['attendance_moments']))
        return new

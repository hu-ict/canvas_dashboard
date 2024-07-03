class AttendanceMoment:
    def __init__(self, attendance_day, points):
        self.attendance_day = attendance_day
        self.points = points

    def to_json(self):
        dict_result = {
            'attendance_day': self.attendance_day,
            'points': self.points
        }
        return dict_result

    def __str__(self):
        return f'Policy({self.attendance_day}, {self.points})'

    @staticmethod
    def from_dict(data_dict):
        # print("Perspective.from_dict", data_dict)
        new = AttendanceMoment(data_dict['attendance_day'], data_dict['points'])
        return new

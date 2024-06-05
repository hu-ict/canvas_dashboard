hover_style=dict(
        bgcolor="#eeeeee",
        font_size=16,
        font_family="Helvetica"
)


def attendance_to_level(a_fraction):
    if a_fraction < 0.10:
        return 0
    elif a_fraction < 0.75:
        return 1
    elif a_fraction < 0.95:
        return 2
    else:
        return 3


def get_marker_size(graded):
    if graded:
        return 14
    else:
        return 9


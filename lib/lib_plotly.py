peil_labels = ["Actueel", "Sprint 4", "Sprint 7", "Beoordeling"]
peil_levels = [-2, -1, 0, 1, 2, 3]
peil_history = {}

hover_style=dict(
        bgcolor="#eeeeee",
        font_size=16,
        font_family="Helvetica"
)

score_binair_dict = {
    -2:{'niveau': 'Open', 'color': 'cornflowerblue'},
    -1:{'niveau': 'Leeg', 'color': '#cccccc'},
    0: {'niveau': 'Niet voldaan', 'color': '#f2a529'},
    1: {'niveau': 'Voldaan', 'color': '#85e043'}
}

def get_score_bin_dict(course_instances):
    if course_instances.is_instance_of('prop_courses'):
        return {"project": score_binair_dict, "final": score_binair_dict, "toets": score_binair_dict}
    elif course_instances.is_instance_of('inno_courses'):
        return {"kennis": score_binair_dict}
    else:
        return {"project": score_binair_dict, "kennis": score_binair_dict}


def get_color_bar(a_start, a_labels_colors):
    colors_bar = {}
    colors_bar["-1"] = a_labels_colors.level_series[a_start.progress.levels].levels["-1"].color
    colors_bar["0"] = a_labels_colors.level_series[a_start.progress.levels].levels["0"].color
    colors_bar["1"] = a_labels_colors.level_series[a_start.progress.levels].levels["1"].color
    colors_bar["2"] = a_labels_colors.level_series[a_start.progress.levels].levels["2"].color
    colors_bar["3"] = a_labels_colors.level_series[a_start.progress.levels].levels["3"].color
    return colors_bar


def fraction_to_level3(a_fraction):
    if a_fraction < 0.01:
        return 0
    elif a_fraction < 0.55:
        return 1
    elif a_fraction < 0.80:
        return 2
    else:
        return 3

def fraction_to_level5(a_fraction):
    if a_fraction < 0.10:
        return 0
    elif a_fraction < 0.40:
        return 1
    elif a_fraction < 0.60:
        return 2
    elif a_fraction < 0.75:
        return 3
    elif a_fraction < 0.85:
        return 4
    else:
        return 5

def attendance_to_level(a_fraction):
    if a_fraction < 0.10:
        return 0
    elif a_fraction < 0.75:
        return 1
    elif a_fraction < 0.95:
        return 2
    else:
        return 3


def fraction_to_bin_level(a_fraction):
    if a_fraction < 0.5:
        return 0
    else:
        return 1


def get_marker_size(graded):
    if graded:
        return 14
    else:
        return 9


from lib.file import tennant

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

if tennant == "prop":
    score_bin_dict = {"project": score_binair_dict, "final": score_binair_dict, "toets": score_binair_dict}
elif tennant == "inno":
    score_bin_dict = {"kennis": score_binair_dict}
else:
    score_bin_dict = {"project": score_binair_dict, "kennis": score_binair_dict}


def get_color_bar(a_course, a_labels_colors):
    colors_bar = {}
    colors_bar["-1"] = a_labels_colors.level_series[a_course.perspectives[a_course.progress_perspective].levels].levels["-1"].color
    colors_bar["0"] = a_labels_colors.level_series[a_course.perspectives[a_course.progress_perspective].levels].levels["0"].color
    colors_bar["1"] = a_labels_colors.level_series[a_course.perspectives[a_course.progress_perspective].levels].levels["1"].color
    colors_bar["2"] = a_labels_colors.level_series[a_course.perspectives[a_course.progress_perspective].levels].levels["2"].color
    colors_bar["3"] = a_labels_colors.level_series[a_course.perspectives[a_course.progress_perspective].levels].levels["3"].color
    return colors_bar


def fraction_to_level(a_fraction):
    if a_fraction < 0.001:
        return 0
    elif a_fraction < 0.55:
        return 1
    elif a_fraction < 0.80:
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


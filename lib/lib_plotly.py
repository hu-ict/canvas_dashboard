plot_path = ".//dashboard - lokaal//plotly//"
template_path_general = ".//dashboard - lokaal//"
source_path = ".//dashboard - lokaal//"

peil_labels = ["Actueel", "Sprint 4", "Sprint 7", "Beoordeling"]
peil_levels = [-2, -1, 0, 1, 2, 3]
peil_history = {}

hover_style=dict(
        bgcolor="#eeeeee",
        font_size=16,
        font_family="Helvetica"
)

score_kennis_bin_dict = {
    -2:{'niveau': 'Leeg', 'color': 'cornflowerblue'},
    -1:{'niveau': 'Leeg', 'color': '#cccccc'},
    0: {'niveau': 'Niet voldaan', 'color': '#f2a529'},
    1: {'niveau': 'Voldaan', 'color': '#85e043'}
}

score_bin_dict = {"kennis": score_kennis_bin_dict}

def get_color_bar(a_course):
    colors_bar = {}
    colors_bar["-1"] = a_course.perspectives["peil"].levels["-1"].color
    colors_bar["-0"] = a_course.perspectives["peil"].levels["0"].color
    colors_bar["1"] = a_course.perspectives["peil"].levels["1"].color
    colors_bar["2"] = a_course.perspectives["peil"].levels["2"].color
    colors_bar["3"] = a_course.perspectives["peil"].levels["3"].color
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


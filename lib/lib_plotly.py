plot_path = ".//dashboard - lokaal//plotly//"
template_path_general = ".//dashboard - lokaal//"
source_path = ".//dashboard - lokaal//"

peil_labels = ["Actueel", "Sprint 4", "Sprint 7", "Beoordeling"]
peil_levels = [-1, 0, 1, 2, 3]
peil_history = {}

hover_style=dict(
        bgcolor="#eeeeee",
        font_size=16,
        font_family="Helvetica"
)

score_team_dict = {
    -2:{'niveau': 'Leeg', 'color': 'cornflowerblue'},
    -1:{'niveau': 'Leeg', 'color': '#cccccc'},
    0: {'niveau': 'Niet zichtbaar', 'color': '#EDF8F0'},
    1: {'niveau': 'Startend', 'color': '#B8E3C4'},
    2: {'niveau': 'Samenwerkend', 'color': '#85e043'},
    3: {'niveau': 'Excellerend', 'color': '#2bad4e'}
}

score_gilde_dict = {
    -2:{'niveau': 'Leeg', 'color': 'cornflowerblue'},
    -1:{'niveau': 'Leeg', 'color': '#cccccc'},
    0: {'niveau': 'Niet zichtbaar', 'color': '#f25829'},
    1: {'niveau': 'Startend', 'color': '#f2a529'},
    2: {'niveau': 'Samenwerkend', 'color': '#85e043'},
    3: {'niveau': 'Excellerend', 'color': '#2bad4e'}
}

score_kennis_dict = {
    -2:{'niveau': 'Leeg', 'color': 'cornflowerblue'},
    -1:{'niveau': 'Leeg', 'color': '#cccccc'},
    0: {'niveau': 'Niet zichtbaar', 'color': '#f25829'},
    1: {'niveau': 'Onder niveau', 'color': '#f2a529'},
    2: {'niveau': 'Op niveau', 'color': '#85e043'},
    3: {'niveau': 'Boven niveau', 'color': '#2bad4e'}
}

score_voortgang_dict = {
    -2:{'niveau': 'Nog niet bepaald', 'color': 'cornflowerblue'},
    -1:{'niveau': 'Leeg', 'color': '#cccccc'},
    0: {'niveau': 'Geen voortgang', 'color': '#f25829'},
    1: {'niveau': 'Onvoldoende voortgang', 'color': '#f2a529'},
    2: {'niveau': 'Voldoende voortgang', 'color': '#85e043'},
    3: {'niveau': 'Goede voortgang', 'color': '#2bad4e'}
}

score_beoordeling_dict = {
    -2:{'niveau': 'Nog niet beoordeeld', 'color': 'cornflowerblue'},
    -1:{'niveau': 'Onbekend', 'color': '#cccccc'},
    0: {'niveau': 'Niet aanwezig', 'color': '#f25829'},
    1: {'niveau': 'Onder niveau', 'color': '#f2a529'},
    2: {'niveau': 'op niveau', 'color': '#85e043'},
    3: {'niveau': 'Boven niveau', 'color': '#2bad4e'}
}

score_dict = {
    "team": score_team_dict,
    "gilde": score_gilde_dict,
    "kennis": score_kennis_dict,
    "voortgang": score_voortgang_dict,
    "beoordeling": score_beoordeling_dict
}

score_kennis_bin_dict = {
    -2:{'niveau': 'Leeg', 'color': 'cornflowerblue'},
    -1:{'niveau': 'Leeg', 'color': '#cccccc'},
    0: {'niveau': 'Niet voldaan', 'color': '#f2a529'},
    1: {'niveau': 'Voldaan', 'color': '#85e043'}
}

score_bin_dict = {"kennis": score_kennis_bin_dict}

colors_bar = {}
colors_bar["-1"] = score_dict['voortgang'][-1]['color']
colors_bar["-0"] = score_dict['voortgang'][0]['color']
colors_bar["1"] = score_dict['voortgang'][1]['color']
colors_bar["2"] = score_dict['voortgang'][2]['color']
colors_bar["3"] = score_dict['voortgang'][3]['color']


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


from scripts.model.dashboard.LevelSerie import LevelSerie

ATTENDANCE_LABELS = {
    "status": {
        "1": {
            "label": "Voor deadline",
            "color": "#BFBFBF"
        },
        "2": {
            "label": "Nog niet beoordeeld",
            "color": "#E97132"
        },
        "3": {
            "label": "Niet correct beoordeeld",
            "color": "#E97132"
        },
        "4": {
            "label": "Niets ingeleverd",
            "color": "#E97132"
        },
        "5": {
            "label": "Beoordeeld",
            "color": "#3C7D22"
        }
    },
    "grades": {
        "0": {
            "level": "0",
            "label": "Niet aanwezig",
            "color": "#B8E3C4",
            "fraction": 0.01,
            "value": 0
        },
        "1": {
            "level": "1",
            "label": "Te laat/vroeg weg",
            "color": "#85e043",
            "fraction": 0.5,
            "value": 0.5
        },
        "2": {
            "level": "2",
            "label": "Aanwezig",
            "color": "#2bad4e",
            "fraction": 1.0,
            "value": 1
        }
    }
}

PROGRESS_LABELS = {
    "status": {
        "1": {
            "label": "Voortgang niet bepaald",
            "color": "#BFBFBF"
        },
        "2": {
            "label": "Voortgang nog niet bepaald",
            "color": "#E97132"
        },
        "3": {
            "label": "Voortgang niet correct bepaald",
            "color": "#E97132"
        },
        "4": {
            "label": "Voortgang niet bepaald",
            "color": "#E97132"
        },
        "5": {
            "label": "Voortgang bepaald",
            "color": "#3C7D22"
        }
    },
    "grades": {
        "-1": {
            "level": "-1",
            "label": "Voortgang niet bepaald",
            "color": "#000000",
            "fraction": 0.00,
            "value": 0
        },
        "0": {
            "level": "0",
            "label": "Voortgang niet zichtbaar",
            "color": "#f25829",
            "fraction": 0.01,
            "value": 0
        },
        "1": {
            "level": "1",
            "label": "Onvoldoende voortgang",
            "color": "#f2a529",
            "fraction": 0.34,
            "value": 0
        },
        "2": {
            "level": "2",
            "label": "Voldoende voortgang",
            "color": "#85e043",
            "fraction": 0.67,
            "value": 0
        },
        "3": {
            "level": "3",
            "label": "Bovengemiddelde voortgang",
            "color": "#2bad4e",
            "fraction": 1.00,
            "value": 0
        }
    }
}

GRADE_LABELS =  {
    "status": {
        "1": {
            "label": "Nog geen beslissing",
            "color": "#BFBFBF"
        },
        "2": {
            "label": "Beslissing nog niet bepaald",
            "color": "#E97132"
        },
        "3": {
            "label": "Beslissing niet correct bepaald",
            "color": "#E97132"
        },
        "4": {
            "label": "Beslissing niet bepaald",
            "color": "#000000"
        },
        "5": {
            "label": "Beslissing bepaald",
            "color": "#3C7D22"
        }
    },
    "grades": {
        "-1": {
            "level": "-1",
            "label": "Beslissing niet bepaald",
            "color": "#000000",
            "fraction": 0.00,
            "value": 0
        },
        "0": {
            "level": "0",
            "label": "Niet zichtbaar",
            "color": "#f25829",
            "fraction": 0.01,
            "value": 0
        },
        "1": {
            "level": "1",
            "label": "Onvoldoende",
            "color": "#f2a529",
            "fraction": 0.01,
            "value": 0
        },
        "2": {
            "level": "2",
            "label": "Voldoende",
            "color": "#85e043",
            "fraction": 0.01,
            "value": 0
        },
        "3": {
            "level": "3",
            "label": "Goed",
            "color": "#2bad4e",
            "fraction": 0.01,
            "value": 0
        },
        "4": {
            "level": "4",
            "label": "Uitmuntend",
            "color": "#2bad4e",
            "fraction": 0.01,
            "value": 0
        },
        "5": {
            "level": "5",
            "label": "Uitmuntend",
            "color": "#2bad4e",
            "fraction": 0.01,
            "value": 0
        }
    }
}


class LevelSerieCollection:
    def __init__(self):

        self.level_series = {}

    def to_json(self):
        dict_result = {}
        for key in self.level_series:
            dict_result[key] = self.level_series[key].to_json()
        return dict_result

    @staticmethod
    def from_dict(data_dict):
        new = LevelSerieCollection()
        for key in data_dict.keys():
            new.level_series[key] = LevelSerie.from_dict(data_dict[key], key)
        return new

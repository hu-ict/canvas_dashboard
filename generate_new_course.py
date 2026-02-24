import json
import os

from canvasapi import Canvas

from scripts.lib.file import read_environment, read_secret_api_key
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, DIR_DIV, SECRET_API_KEY_FILE_NAME
from scripts.lib.lib_date import API_URL
from scripts.model.dashboard.Dashboard import Dashboard
from scripts.model.dashboard.LevelSerieCollection import PROGRESS_LABELS, GRADE_LABELS, ATTENDANCE_LABELS, \
    LevelSerieCollection
from scripts.model.dashboard.MetaAssignmentGroup import MetaAssignmentGroup
from scripts.model.dashboard.Subplot import Subplot
from scripts.model.environment.Course import Course

environment = read_environment(ENVIRONMENT_FILE_NAME)
course_code = input("Give the course_code for the new course: ")
if course_code in environment.get_course_names():
    print("course_code already exists", course_code, environment.get_course_names())
    course_instance_name = input("Give the course_code for the new course: ")
print("Creating new course", course_code)
course = Course(course_code)
environment.courses.append(course)

os.makedirs(os.path.dirname(course.get_path()), exist_ok=True)

with open(ENVIRONMENT_FILE_NAME, 'w') as f:
    dict_result = environment.to_json()
    json.dump(dict_result, f, indent=2)

if course_code in ["TICT-V1SE1-24", "TICT-V1SE1-24A", "TICT-V1SE1-24B"]:
    dashboard_tabs = {
        "groups": "Groepen"
      }

    student_tabs = {
        "portfolio": "Portfolio",
        "voortgang": "Voortgang"
      }
    subplot = Subplot(2, 2, [
          "Kennis",
          "Orientatie",
          "Project skills",
          "Aanwezigheid"
        ], {
          "kennis": {
            "row": 1,
            "col": 1
          },
          "verbreding": {
            "row": 1,
            "col": 2
          },
          "skills": {
            "row": 2,
            "col": 1
          },
          "attendance": {
            "row": 2,
            "col": 2
          }
        }, [[
            {
              "type": "scatter"
            },
            {
              "type": "scatter"
            }
          ],
          [
            {
              "type": "scatter"
            },
            {
              "type": "scatter"
            }
          ]])

    project_group_name=  "SECTIONS"
    guild_group_name = ""
    feedback_colors = {
        "-": {
            "color": "#EDF8F0"
        },
        "N": {
            "color": "#B8E3C4"
        },
        "+": {
            "color": "#85e043"
        }
    }

    level_serie_collection_dict = {
        "bin2": {
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
                    "label": "Niet gemaakt",
                    "color": "#000000"
                },
                "5": {
                    "label": "Beoordeeld",
                    "color": "#3C7D22"
                }
            },
            "grades": {
                "0": {
                    "level": "0",
                    "label": "Niet voldaan",
                    "color": "#0070C0",
                    "fraction": 0.00,
                    "value": 0
                },
                "1": {
                    "level": "1",
                    "label": "Niet voldaan",
                    "color": "#0070C0",
                    "fraction": 0.99,
                    "value": 0
                },
                "2": {
                    "level": "2",
                    "label": "Voldaan",
                    "color": "#3C7D22",
                    "fraction": 1.0,
                    "value": 1
                }
            }
        },
        "attendance": ATTENDANCE_LABELS,
        "progress": PROGRESS_LABELS,
        "grade": GRADE_LABELS
    }

    level_serie_collection = LevelSerieCollection.from_dict(level_serie_collection_dict)

else:
    dashboard_tabs = {
        "groups": "Groepen",
        "guilds": "Gilden",
        "roles": "Rollen"
    }

    student_tabs = {
        "voortgang": "Voortgang",
        "feedback": "Feedback"
    }
    subplot = {
        "rows": 2,
        "cols": 1,
        "titles": [
            "Tijdlijn",
            "Portfolio"
        ],
        "positions": {
            "timeline": {
                "row": 1,
                "col": 1
            },
            "portfolio": {
                "row": 2,
                "col": 1
            }
        },
        "specs": [
            [
                {
                    "type": "scatter"
                }
            ],
            [
                {
                    "type": "scatter"
                }
            ]
        ]
    }
    project_group_name = "Project Groups"
    guild_group_name = "Guild Groups"
    feedback_colors = {
        "-": {
            "color": "#EDF8F0"
        },
        "N": {
            "color": "#B8E3C4"
        },
        "+": {
            "color": "#85e043"
        }
    },
    level_serie_collection_dict = {
        "samen": {
            "status": {
                "1": {
                    "label": "Voor deadline",
                    "color": "#aaaaaa"
                },
                "2": {
                    "label": "Nog niet gewaardeerd",
                    "color": "CornflowerBlue"
                },
                "3": {
                    "label": "Niet correct gewaardeerd",
                    "color": "CornflowerBlue"
                },
                "4": {
                    "label": "Niets ingeleverd",
                    "color": "#f25829"
                },
                "5": {
                    "label": "Gewaardeerd",
                    "color": "#3C7D22"
                }
            },
            "grades": {
                "0": {
                    "level": "0",
                    "label": "Niet zichtbaar",
                    "color": "#EDF8F0",
                    "fraction": 0.1,
                    "value": 0
                },
                "1": {
                    "level": "1",
                    "label": "Startend",
                    "color": "#B8E3C4",
                    "fraction": 0.55,
                    "value": 1
                },
                "2": {
                    "level": "2",
                    "label": "Samenwerkend",
                    "color": "#85e043",
                    "fraction": 0.8,
                    "value": 1
                },
                "3": {
                    "level": "3",
                    "label": "Excellerend",
                    "color": "#2bad4e",
                    "fraction": 1.0,
                    "value": 1
                }
            }
        },
        "gilde": {
            "status": {
                "1": {
                    "label": "Voor deadline",
                    "color": "#aaaaaa"
                },
                "2": {
                    "label": "Nog niet gewaardeerd",
                    "color": "CornflowerBlue"
                },
                "3": {
                    "label": "Niet correct gewaardeerd",
                    "color": "CornflowerBlue"
                },
                "4": {
                    "label": "Niets ingeleverd",
                    "color": "#f25829"
                },
                "5": {
                    "label": "Gewaardeerd",
                    "color": "#3C7D22"
                }
            },
            "grades": {
                "0": {
                    "level": "0",
                    "label": "Niet aanwezig",
                    "color": "#f25829",
                    "fraction": 0.01,
                    "value": 1
                },
                "1": {
                    "level": "1",
                    "label": "Aanwezig en passief",
                    "color": "#85e043",
                    "fraction": 0.55,
                    "value": 1
                },
                "2": {
                    "level": "2",
                    "label": "Aanwezig en passief",
                    "color": "#85e043",
                    "fraction": 0.8,
                    "value": 1
                },
                "3": {
                    "level": "3",
                    "label": "Aanwezig en actief",
                    "color": "#2bad4e",
                    "fraction": 1.0,
                    "value": 1
                }
            }
        },
        "niveau": {
            "status": {
                "1": {
                    "label": "Voor deadline",
                    "color": "#aaaaaa"
                },
                "2": {
                    "label": "Nog niet gewaardeerd",
                    "color": "CornflowerBlue"
                },
                "3": {
                    "label": "Niet correct gewaardeerd",
                    "color": "CornflowerBlue"
                },
                "4": {
                    "label": "Niets ingeleverd",
                    "color": "#f25829"
                },
                "5": {
                    "label": "Gewaardeerd",
                    "color": "#3C7D22"
                }
            },
            "grades": {
                "0": {
                    "level": "0",
                    "label": "Niet zichtbaar",
                    "color": "#f25829",
                    "fraction": 0.01,
                    "value": 1
                },
                "1": {
                    "level": "1",
                    "label": "Onder niveau",
                    "color": "#f2a529",
                    "fraction": 0.55,
                    "value": 1
                },
                "2": {
                    "level": "2",
                    "label": "Op niveau",
                    "color": "#85e043",
                    "fraction": 0.8,
                    "value": 1
                },
                "3": {
                    "level": "3",
                    "label": "Boven niveau",
                    "color": "#2bad4e",
                    "fraction": 1.0,
                    "value": 1
                }
            }
        },
        "attendance": None,
        "progress": PROGRESS_LABELS,
        "grade": GRADE_LABELS
    }
    level_serie_collection = LevelSerieCollection.from_dict(level_serie_collection_dict)
# Initialize a new Canvas object

secret_api_key = read_secret_api_key(SECRET_API_KEY_FILE_NAME)
canvas = Canvas(API_URL, secret_api_key.canvas_api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course_id = input("Give the course_id for the new course, only for assignment_groups: ")
canvas_course = canvas.get_course(canvas_course_id)
canvas_assignment_groups = canvas_course.get_assignment_groups()

dashboard = Dashboard(dashboard_tabs, student_tabs, subplot, project_group_name, guild_group_name, feedback_colors, level_serie_collection)
for canvas_assignment_group in canvas_assignment_groups:
    yes_no = input(f"AssignmentGroup behouden {canvas_assignment_group.name} [enter or n]")
    if 'n' not in yes_no.lower():
        meta_assignment_group = MetaAssignmentGroup(canvas_assignment_group.name, "groups", "strategy", "levels", "marker", 0, 0, 0, 0, 0)
        dashboard.assignment_groups.append(meta_assignment_group)

dashboard_file_name = course.get_path() + DIR_DIV + "dashboard.json"
with open(dashboard_file_name, 'w') as f:
    dict_result = dashboard.to_json()
    json.dump(dict_result, f, indent=2)
print("Course is created", course_code)

# -*- coding: utf-8 -*-
#
import json
import os

from canvasapi import Canvas

from scripts.lib.file import read_environment, read_secret_api_key
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, DIR_DIV, SECRET_API_KEY_FILE_NAME
from scripts.lib.lib_date import API_URL
from scripts.lib.lib_learning_outcomes import learning_outcomes_V1SE1, learning_outcomes_V3SE6
from scripts.model.Role import Role
from scripts.model.dashboard.Dashboard import Dashboard
from scripts.model.dashboard.Groups import Groups
from scripts.model.dashboard.LevelSerieCollection import PROGRESS_LABELS, GRADE_LABELS, ATTENDANCE_LABELS, \
    LevelSerieCollection, BIN2, NIVEAU, GILDE, SAMEN
from scripts.model.dashboard.MetaAssignmentGroup import MetaAssignmentGroup
from scripts.model.dashboard.Subplot import Subplot
from scripts.model.environment.Course import Course

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
positions = {
    "timeline": {"row": 1, "col": 1},
    "portfolio": {"row": 2, "col": 1 }
    }

specs = [[{"type": "scatter"}],
        [{"type": "scatter"}]]

titles = ["Tijdlijn", "Portfolio"]
subplot = Subplot(2, 1, titles,  positions, specs)

environment = read_environment(ENVIRONMENT_FILE_NAME)
course_code = input("Give the course_code for the new course: ")
while course_code in environment.get_course_names():
    print("course_code already exists", course_code, environment.get_course_names())
    course_code = input("Give the course_code for the new course: ")
print("Creating new course", course_code)
course = Course(course_code)
environment.courses.append(course)

os.makedirs(os.path.dirname(course.get_path()), exist_ok=True)

with open(ENVIRONMENT_FILE_NAME, 'w') as f:
    dict_result = environment.to_json()
    json.dump(dict_result, f, indent=2)

if course_code in ["TICT-V1SE1-24", "TICT-V1SE1-24a"]:
    dashboard_tabs = {
        "groups_1": "groups_1",
        "groups_2": "groups_2",
        "roles": "Rollen",
        "levels": "Voortgang",
        "workload": "Werkvoorraad",
        "learning_outcomes": "Leeruitkomsten",
        "release_planning": "Release Planning",
        "learning_analytics": "Learning analytics"
    }
    roles = []
    roles.append(Role("role", "Student", "HBO-ICT", "border-dark"))

    groups_1 = Groups("Klas", "SECTIONS", "Beoordelingsmomenten")
    groups_2 = Groups("Leerteam", "Leerteams", "")
    learning_outcomes = learning_outcomes_V1SE1
    student_tabs = {
        "portfolio": "Portfolio",
        "voortgang": "Voortgang"
      }


    level_serie_collection_dict = {
        "bin2": BIN2,
        "attendance": ATTENDANCE_LABELS,
        "progress": PROGRESS_LABELS,
        "grade": GRADE_LABELS
    }

    level_serie_collection = LevelSerieCollection.from_dict(level_serie_collection_dict)
    perspectives = [
      {
        "name": "portfolio",
        "title": "Portfolio",
        "show_flow": False,
        "show_points": True,
        "assignment_group_names": ["Kennis", "Oriëntatie op afstudeerrichtingen", "Professionele Vermogens & Project"]
      }

    ]
    level_moments = {"name": "level_moments", "title": "Peilmomenten", "assignment_group_names": ["Voortgangsmomenten"]}
    grade_moments = {"name": "grade_moments", "title": "Beoordelingsmomenten", "assignment_group_names": ["Beoordelingsmomenten"]}
else:
    dashboard_tabs = {
        "groups_1": "groups_1",
        "groups_2": "groups_2",
        "roles": "Rollen",
        "levels": "Voortgang",
        "workload": "Werkvoorraad",
        "learning_outcomes": "Leeruitkomsten",
        "release_planning": "Release Planning",
        "learning_analytics": "Learning analytics"
    }
    groups_1 = Groups("Projecten", "Project Groups", "Beoordelingsmomenten")
    groups_2 = Groups("Gilden", "Guild Groups", "Gilde")
    learning_outcomes = learning_outcomes_V3SE6
    level_moments = {"name": "level_moments", "title": "Peilmomenten", "assignment_group_names": ["Peilmomenten"]}
    grade_moments = {"name": "grade_moments", "title": "Beoordelingsmomenten", "assignment_group_names": ["Beoordelingsmomenten"]}
    student_tabs = {
        "voortgang": "Voortgang",
        "feedback": "Feedback"
    }

    level_serie_collection_dict = {
        "samen": SAMEN,
        "gilde": GILDE,
        "niveau": NIVEAU,
        "attendance": None,
        "progress": PROGRESS_LABELS,
        "grade": GRADE_LABELS
    }
    level_serie_collection = LevelSerieCollection.from_dict(level_serie_collection_dict)
    roles = []
    perspectives = [
      {
        "name": "portfolio",
        "title": "Portfolio",
        "show_flow": True,
        "show_points": False,
        "assignment_group_names": ["Project", "Gilde", "Hackathon", "User Stories in project"]

      }
    ]

# Initialize a new Canvas object

secret_api_key = read_secret_api_key(SECRET_API_KEY_FILE_NAME)
canvas = Canvas(API_URL, secret_api_key.canvas_api_key)
user = canvas.get_current_user()
print(user.name)
canvas_course_id = input("Give the course_id for the new course, only for assignment_groups: ")
canvas_course = canvas.get_course(canvas_course_id)
canvas_assignment_groups = canvas_course.get_assignment_groups()


dashboard = Dashboard(dashboard_tabs, student_tabs, subplot, feedback_colors, level_serie_collection)
dashboard.groups_1 = groups_1
dashboard.groups_2 = groups_2
dashboard.learning_outcomes = learning_outcomes
dashboard.perspectives = perspectives
dashboard.level_moments = level_moments
dashboard.grade_moments = grade_moments
dashboard.roles = roles
for canvas_assignment_group in canvas_assignment_groups:
    yes_no = input(f"AssignmentGroup behouden {canvas_assignment_group.name} [enter or n]")
    if 'n' not in yes_no.lower():
        meta_assignment_group = MetaAssignmentGroup(canvas_assignment_group.name, "groups_1", "POINTS", "bin2", "circle", 0, 0, 0, 0, 0)
        dashboard.assignment_groups.append(meta_assignment_group)

dashboard_file_name = course.get_path() + DIR_DIV + "dashboard.json"
with open(dashboard_file_name, 'w') as f:
    dict_result = dashboard.to_json()
    json.dump(dict_result, f, indent=2)
print("Course is created", course_code)

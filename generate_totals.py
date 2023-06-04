from datetime import datetime
from operator import itemgetter

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import numpy as np

from lib.config import plot_path, voortgang_tabel, color_tabel, hover_style, peil_labels
from lib.file import read_course_config_start, read_course, read_results

course_config_start = read_course_config_start()
course = read_course(course_config_start.course_file_name)
results = read_results(course_config_start.results_file_name)
actual_day = (results.actual_date - course_config_start.start_date).days

student_totals = {}
# for perspective in course.perspectives:
#     student_totals[perspective.name] = {}
#     for teacher in course.

student_totals = {
    'student_count': 0,
    'team': {'count': [], 'pending': {'BW': 0, 'MB': 0, 'KE': 0, 'TPM': 0, 'PVR': 0, 'MVD': 0, 'HVG': 0}, 'late': {'BW': 0, 'MB': 0, 'KE': 0, 'TPM': 0, 'PVR': 0, 'MVD': 0, 'HVG': 0}, 'to_late': {'BW': 0, 'MB': 0, 'KE': 0, 'TPM': 0, 'PVR': 0, 'MVD': 0, 'HVG': 0}},
    'gilde': {'count': [], 'pending': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}, 'late': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}, 'to_late': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}},
    'kennis': {'count': [], 'pending': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}, 'late': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}, 'to_late': {'AI': 0, 'BIM': 0, 'CSC': 0, 'SD_B': 0, 'SD_F': 0, 'TI': 0}},
    'peil': {
        'halfweg': {0: 0, 1: 0, 2: 0, 3: 0},
        'eind': {0: 0, 1: 0, 2: 0, 3: 0}
    },
    'late': {'count': []}
}

late_list = []

submissions_late = {
    'team': {'BW': [], 'MB': [], 'KE': [], 'TPM': [], 'PVR': [], 'MVD': [], 'HVG': []},
    'gilde': {'AI': [], 'BIM': [], 'CSC': [], 'SD_B': [], 'SD_F': [], 'TI': []},
    'kennis': {'AI': [], 'BIM': [], 'CSC': [], 'SD_B': [], 'SD_F': [], 'TI': []}
}


def student_total(perspective):
    cum_score = 0
    for submission in perspective:
        cum_score += submission.score
    return cum_score


def get_peil(perspective, query):
    for submission in perspective:
        condition = 0
        for item in query:
            if item in submission.assignment_name:
                condition += 1
        if condition == len(query):
            return int(submission.score)
    return -1


def add_total(totals, total):
    totals.append(total)
    # if total not in totals.keys():
    #     totals[total] = 1
    # else:
    #     totals[total] += 1


def get_submitted_at(item):
    return item.submitted_at


def count_student(course_config, student):
    for perspective in student.perspectives:
        if perspective.name == "peil":
            student_totals[perspective.name]["halfweg"][get_peil(perspective.submissions, ["halfweg", "Overall"])] += 1
        elif perspective.name == "kennis":
            add_total(student_totals[perspective.name]['count'], int(student_total(perspective.submissions)))
        else:
            add_total(student_totals[perspective.name]['count'], int(student_total(perspective.submissions)))

    # role = student.get_role()
    # total_points = course_config.find_assignment_group_by_role(role).total_points
    # add_total(student_totals['kennis']['count'], int(student_total(student.kennis)/total_points*100))


def check_for_late(student, submission, perspective):
    if not submission.graded:
        if student.coach_initials != "None":
            if perspective == 'team':
                selector = student.coach_initials
            else:
                selector = student.get_role()
        else:
            selector = student.get_role()
        late_days = (results.actual_date - submission.submitted_at).days
        if late_days <= 7:
            student_totals[perspective]['pending'][selector] += 1
        elif 7 < late_days <= 14:
            student_totals[perspective]['late'][selector] += 1
            submissions_late[perspective][selector].append(submission.to_json())
        else:
            late_list.append(submission.to_json())
            submissions_late[perspective][selector].append(submission.to_json())
            student_totals[perspective]['to_late'][selector] += 1
        add_total(student_totals['late']['count'], late_days)


def plot_totals():
    titles = ["Team", "Gilde", 'Kennis', 'Team', 'Gilde', 'Kennis', 'Halfweg', 'Eind', 'Vertraging']
    specs = [
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}],
        [{'type': 'domain'}, {'type': 'domain'}, None],
        [{'type': 'bar'}, None, None]
    ]

    fig = make_subplots(rows=4, cols=3, specs=specs, subplot_titles=titles)
    fig.update_layout(height=1400, width=1200, showlegend=False)
    data = go.Histogram(x=np.array(student_totals['team']['count']))
    fig.add_trace(data, 1, 1)
    data = go.Histogram(x=np.array(student_totals['gilde']['count']), marker=dict(color="#f6c23e"))
    fig.add_trace(data, 1, 2)
    data = go.Histogram(x=np.array(student_totals['kennis']['count']))
    fig.add_trace(data, 1, 3)

    fig.update_xaxes(title_text="Punten")

    fig.update_layout(
        title_text='Scores studenten',  # title of plot
        xaxis_title_text='Punten',  # xaxis label
        xaxis2_title_text='Punten',  # xaxis label
        xaxis3_title_text='Percentage',  # xaxis label
        xaxis4_title_text='Pending',  # xaxis label
        xaxis5_title_text='Pending',  # xaxis label
        xaxis6_title_text='Pending',  # xaxis label
        xaxis7_title_text='Dagen na inlevering',  # xaxis label
        yaxis_title_text='Aantal',  # yaxis label
        yaxis4_title_text='Aantal',  # yaxis label
        # yaxis9_title_text='Aantal',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # gap between bars of the same location coordinates
        barmode='stack'
    )
    for student_group in results.studentGroups:
        for student in student_group.students:
            for perspective in student.perspectives:
                for submission in perspective.submissions:
                    check_for_late(student, submission, perspective.name)

    col = 0
    for perspective in course.perspectives:
        if perspective.name != course_config_start.peil_perspective:
            col += 1
            x_team = list(student_totals[perspective.name]['pending'].keys())
            y_counts = list(student_totals[perspective.name]['pending'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Pending", marker=dict(color="#4e73df")), 2, col)
            x_team = list(student_totals[perspective.name]['late'].keys())
            y_counts = list(student_totals[perspective.name]['late'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Late", marker=dict(color="#e74a3b")), 2, col)
            x_team = list(student_totals[perspective.name]['to_late'].keys())
            y_counts = list(student_totals[perspective.name]['to_late'].values())
            fig.add_trace(go.Bar(x=x_team, y=y_counts, name="To Late", marker=dict(color="#555555")), 2, col)

    data = go.Histogram(x=np.array(student_totals['late']['count']))
    fig.add_trace(data, 4, 1)

    col = 0
    for peil_label in peil_labels:
        col += 1
        print(student_totals['peil'][peil_label].items())
        values = []
        labels = []
        colors = []
        for value in student_totals['peil'][peil_label].values():
            values.append(value)
        for key in student_totals['peil'][peil_label].keys():
            labels.append(voortgang_tabel[key])
        for color in color_tabel.values():
            colors.append(color)
        # print(labels)
        # print(values)
        # print(colors)
        trace = go.Pie(
            values=values,
            labels=labels, marker_colors=colors,
            direction='clockwise',
            sort=False, hoverlabel=hover_style)
        # data = [trace]
        # fig = go.Figure(data=data)

        fig.add_trace(
            trace,
            3, col)

    file_name = plot_path + "totals" + ".html"
    fig.write_html(file_name, include_plotlyjs="cdn")


for group in results.studentGroups:
    for student in group.students:
        count_student(course, student)

plot_totals()

late_list = sorted(late_list, key=itemgetter('submitted_at'))

with open("late.json", 'w') as f:
    json.dump(late_list, f, indent=2)

for perspective in submissions_late.keys():
    print(perspective)
    for selector in submissions_late[perspective].keys():
        print(selector)
        late_list = sorted(submissions_late[perspective][selector], key=itemgetter('submitted_at'))

        with open("late_"+perspective+"_"+selector+".json", 'w') as f:
            json.dump(late_list, f, indent=2)


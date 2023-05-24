from datetime import datetime
from operator import itemgetter

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import numpy as np

from lib.config import plot_path
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
    'late': {'count': []}
}

late_list = []

def student_total(perspective):
    cum_score = 0
    for submission in perspective:
        cum_score += submission.score
    return cum_score


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
        if perspective.name != "peil":
            add_total(student_totals[perspective.name]['count'], int(student_total(perspective.submissions)))

    # role = student.get_role()
    # total_points = course_config.find_assignment_group_by_role(role).total_points
    # add_total(student_totals['kennis']['count'], int(student_total(student.kennis)/total_points*100))


def check_for_late(student, submission, perspective):
    if not submission.graded and student.coach_initials != "None":
        if perspective == 'team':
            selector = student.coach_initials
        else:
            selector = student.get_role()
        late_days = (results.actual_date - submission.submitted_at).days
        if late_days <= 7:
            student_totals[perspective]['pending'][selector] += 1
        elif 7 < late_days <= 14:
            student_totals[perspective]['late'][selector] += 1
        else:
            late_list.append(submission.to_json())
            student_totals[perspective]['to_late'][selector] += 1
        add_total(student_totals['late']['count'], late_days)


def plot_totals():
    titles = ["Team", "Gilde", 'Kennis', 'Team', 'Gilde', 'Kennis', 'Vertraging']
    fig = make_subplots(rows=3, cols=3, subplot_titles=titles)
    fig.update_layout(height=1000, width=1200, showlegend=False)
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
        yaxis7_title_text='Aantal',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # gap between bars of the same location coordinates
        barmode='stack'
    )
    for student_group in results.studentGroups:
        for student in student_group.students:
            for perspective in student.perspectives:
                for submission in perspective.submissions:
                    check_for_late(student, submission, perspective.name)

    x_team = list(student_totals['team']['pending'].keys())
    y_counts = list(student_totals['team']['pending'].values())
    fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Pending", marker=dict(color="#4e73df")), 2, 1)

    x_team = list(student_totals['team']['late'].keys())
    y_counts = list(student_totals['team']['late'].values())
    fig.add_trace(go.Bar(x=x_team, y=y_counts, name="Late", marker=dict(color="#e74a3b")), 2, 1)

    x_team = list(student_totals['team']['to_late'].keys())
    y_counts = list(student_totals['team']['to_late'].values())
    fig.add_trace(go.Bar(x=x_team, y=y_counts, name="To Late", marker=dict(color="#555555")), 2, 1)

    x_gilde = list(student_totals['gilde']['pending'].keys())
    y_counts = list(student_totals['gilde']['pending'].values())
    fig.add_trace(go.Bar(x=x_gilde, y=y_counts, name="Pending", marker=dict(color="#4e73df")), 2, 2)

    x_gilde = list(student_totals['gilde']['late'].keys())
    y_counts = list(student_totals['gilde']['late'].values())
    fig.add_trace(go.Bar(x=x_gilde, y=y_counts, name="Late", marker=dict(color="#e74a3b")), 2, 2)

    x_gilde = list(student_totals['gilde']['to_late'].keys())
    y_counts = list(student_totals['gilde']['to_late'].values())
    fig.add_trace(go.Bar(x=x_gilde, y=y_counts, name="To late", marker=dict(color="#555555")), 2, 2)

    x_kennis = list(student_totals['kennis']['pending'].keys())
    y_counts = list(student_totals['kennis']['pending'].values())
    fig.add_trace(go.Bar(x=x_kennis, y=y_counts, name="Pending", marker=dict(color="#4e73df")), 2, 3)

    x_kennis = list(student_totals['kennis']['late'].keys())
    y_counts = list(student_totals['kennis']['late'].values())
    fig.add_trace(go.Bar(x=x_kennis, y=y_counts, name="Late", marker=dict(color="#e74a3b")), 2, 3)

    x_kennis = list(student_totals['kennis']['to_late'].keys())
    y_counts = list(student_totals['kennis']['to_late'].values())
    fig.add_trace(go.Bar(x=x_kennis, y=y_counts, name="To late", marker=dict(color="#555555")), 2, 3)


    data = go.Histogram(x=np.array(student_totals['late']['count']))
    fig.add_trace(data, 3, 1)

    file_name = plot_path + "totals" + ".html"
    fig.write_html(file_name, include_plotlyjs="cdn")


for group in results.studentGroups:
    for student in group.students:
        count_student(course, student)

plot_totals()

late_list = sorted(late_list, key=itemgetter('submitted_at'))

with open("late.json", 'w') as f:
    json.dump(late_list, f, indent=2)

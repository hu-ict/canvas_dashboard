import sys
from lib.lib_date import get_actual_date
from lib.file import read_course, read_results, read_course_instances
import numpy as np
import plotly.graph_objs as go


def generate_dashboard(instance_name):
    print("GT01 - generate_top.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("GT02 - Instance:", instance.name)
    course = read_course(instance.get_course_file_name())
    team_scores = {}
    for group in course.student_groups:
        team_scores[group.id] = {"team": group.name, "score": 0, "scores": []}
    results = read_results(instance.get_result_file_name())
    scores = {"team": [], "gilde": [], "kennis": []}
    # scores = {"kennis": [], "verbreding": [], "skills": []}
    for student in results.students:
        for perspective in student.perspectives:
            if perspective == 'kennis':
                if student.role not in scores:
                    scores[student.role] = []
                scores[student.role].append(student.perspectives[perspective].sum_score)
            else:
                scores[perspective].append(student.perspectives[perspective].sum_score)
    high_scores = {"BIM": max(scores["BIM"]), "CSC_C": max(scores["CSC_C"]), "CSC_S": max(scores["CSC_S"]), "SD_B": max(scores["SD_B"]), "TI": max(scores["TI"]), "gilde": max(scores["gilde"]), "team": max(scores["team"])}
    # high_scores = {"kennis": max(scores["kennis"]), "verbreding": max(scores["verbreding"]), "skills": max(scores["skills"])}
    print(high_scores)
    student_scores = []
    for student in results.students:
        student_score = 0
        for perspective in student.perspectives:
            if perspective == "kennis":
                student_score += student.perspectives[perspective].sum_score / high_scores[student.role]
            else:
                student_score += student.perspectives[perspective].sum_score / high_scores[perspective]
        student_scores.append({"student": student.name, "score": student_score})
        team_scores[student.group_id]["scores"].append(student_score)
    student_scores = sorted(student_scores, key=lambda s: s["score"])
    for score in student_scores:
        print("Student", score["student"], int(score["score"]*100)/100)
    team_scores = list(team_scores.values())
    for team in team_scores:
        if len(team["scores"]) != 0:
            team_score = sum(team["scores"])/len(team["scores"])
        else:
            team_score = 0
        team["score"] = int(team_score*100)/100
    team_scores = sorted(team_scores, key=lambda s: s["score"])
    for team in team_scores:
        print("Team", team["team"], team["score"])
    print("GT99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

    student_score_freq = []
    for score in team_scores:
        student_score_freq.append(score["score"])

    # counts, bins = np.histogram(student_score_freq, bins=range(0, 3, 1))
    # bins = 0.5 * (bins[:-1] + bins[1:])
    fig = go.Figure(data=[go.Histogram(x=student_score_freq)])
    fig.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_dashboard(sys.argv[1])
    else:
        generate_dashboard("")

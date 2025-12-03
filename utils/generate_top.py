import sys
from lib.lib_date import get_actual_date
from lib.file import read_course, read_results, read_course_instances


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
    for group in course.project_groups:
        team_scores[group.id] = {"team": group.name, "score": 0, "scores": []}
    results = read_results(instance.get_result_file_name())
    scores_k = {"team": [], "gilde": [], "kennis": []}
    scores_p = {"kennis": [], "verbreding": [], "skills": []}
    for student_results in results.students:
        for perspective in student_results.perspectives:
            if perspective == 'kennis':
                if student_results.role not in scores_k:
                    scores_k[student_results.role] = []
                scores_k[student_results.role].append(student_results.perspectives[perspective].sum_score)
            else:
                scores_k[perspective].append(student_results.perspectives[perspective].sum_score)
    high_scores_k = {"AI": max(scores_k["AI"]), "BIM": max(scores_k["BIM"]), "CSC_S": max(scores_k["CSC_S"]), "SD_B": max(scores_k["SD_B"]), "SD_F": max(scores_k["SD_F"]), "gilde": max(scores_k["gilde"]), "team": max(scores_k["team"])}
    # high_scores = {"kennis": max(scores["kennis"]), "verbreding": max(scores["verbreding"]), "skills": max(scores["skills"])}
    print(high_scores_k)
    student_scores = []
    for student_results in results.students:
        student = course.find_student(student_results.id)
        student_score = 0
        student_perspective_score = {}
        for perspective in student_results.perspectives:
            if perspective == "kennis":
                # continue
                student_score += student_results.perspectives[perspective].sum_score / high_scores_k[student.role]
                student_perspective_score[perspective] = round(student_results.perspectives[perspective].sum_score / high_scores_k[student.role], 2)
            else:
                student_score += student_results.perspectives[perspective].sum_score / high_scores_k[perspective]
                student_perspective_score[perspective] = round(student_results.perspectives[perspective].sum_score / high_scores_k[perspective], 2)
        print(student_results.name, round(student_score, 2), student_perspective_score)
        student_scores.append({"student": student_results.name, "score": student_score})
        team_scores[student.project_id]["scores"].append(student_score)
    student_scores = sorted(student_scores, key=lambda s: s["score"], reverse=True)
    for score in student_scores:
        print("Student", score["student"], int(score["score"]*100)/100)
    team_scores = list(team_scores.values())
    for team in team_scores:
        if len(team["scores"]) != 0:
            team_score = sum(team["scores"])/len(team["scores"])
        else:
            team_score = 0
        team["score"] = int(team_score*100)/100
    team_scores = sorted(team_scores, key=lambda s: s["score"], reverse=True)
    for team in team_scores:
        print("Team", team["team"], team["score"])
    print("GT99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

    # student_score_freq = []
    # for score in team_scores:
    #     student_score_freq.append(score["score"])

    # counts, bins = np.histogram(student_score_freq, bins=range(0, 3, 1))
    # bins = 0.5 * (bins[:-1] + bins[1:])
    # fig = go.Figure(data=[go.Histogram(x=student_score_freq)])
    # fig.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_dashboard(sys.argv[1])
    else:
        generate_dashboard("")

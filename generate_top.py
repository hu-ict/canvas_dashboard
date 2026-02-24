import sys

from scripts.lib.file_const import ENVIRONMENT_FILE_NAME
from scripts.lib.lib_date import get_actual_date, get_date_time_obj
from scripts.lib.file import read_course, read_results, read_environment


def run_env_4(a_actual_date):
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    execution = environment.get_execution_by_name("env_3")
    for course in environment.courses:
        for course_instance in course.course_instances:
            if get_date_time_obj(course_instance.period["end_date"]) > a_actual_date and course_instance.stage != "SLEEP":
                print("Instance:", course_instance.name)
                course_instance.execution_source_path = execution.source_path
                generate_top(course_instance)


def generate_top(course_instance):
    print("GT02 - Instance:", course_instance.name)
    course = read_course(course_instance.get_course_file_name())
    team_scores = {}
    for group in course.project_groups:
        team_scores[group.id] = {"team": group.name, "score": 0, "scores": []}
    results = read_results(course_instance.get_result_file_name())
    scores_k = {"portfolio": []}
    for student_results in results.students:
        for perspective in student_results.perspectives:
            scores_k[perspective].append(student_results.perspectives[perspective].sum_score)
    high_scores_portfolio = max(scores_k["portfolio"])
    print(high_scores_portfolio)
    student_scores = []
    for student_results in results.students:
        student = course.find_student(student_results.id)
        student_score = 0
        student_perspective_score = {}
        for perspective in student_results.perspectives:
            student_score += student_results.perspectives[perspective].sum_score / high_scores_portfolio
            student_perspective_score[perspective] = round(student_results.perspectives[perspective].sum_score / high_scores_portfolio, 2)
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

    # student_score_freq = []
    # for score in team_scores:
    #     student_score_freq.append(score["score"])

    # counts, bins = np.histogram(student_score_freq, bins=range(0, 3, 1))
    # bins = 0.5 * (bins[:-1] + bins[1:])
    # fig = go.Figure(data=[go.Histogram(x=student_score_freq)])
    # fig.show()

if __name__ == "__main__":
    l_actual_date = get_actual_date()
    sys.stdout.reconfigure(encoding="utf-8")
    run_env_4(l_actual_date)
    total_seconds = (get_actual_date() - l_actual_date).seconds
    seconds = total_seconds % 60
    minutes = total_seconds // 60
    print(f"Time running: {minutes}:{seconds:02d} (m:ss)")
    print("Time running:", total_seconds, "seconds")
    print("Date running:", get_actual_date())

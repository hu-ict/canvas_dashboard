import sys

from scripts.lib.file_const import ENVIRONMENT_FILE_NAME
from scripts.lib.lib_date import get_actual_date, get_date_time_obj
from scripts.lib.file import read_course, read_results, read_environment

def write_feedback_csv(filename, feedback_list):
    print('CSV01 - write_feedback_csv', filename)
    with open(filename, 'w', encoding="utf-8") as csvfile:
        csvfile.write('dag;pos_neg;canvas_opdracht;waardering;feedback\n')
        for feedback in feedback_list:
            csvfile.write(str(feedback.day) + ";" + feedback.positive_neutral_negative + ';"' + feedback.assignment_name + '";' + str(int(feedback.grade)) + ';"' + feedback.comment + '"\n')


def run_env_4(a_actual_date):
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    execution = environment.get_execution_by_name("env_3")
    for course in environment.courses:
        for course_instance in course.course_instances:
            if course_instance.stage != "SLEEP": #get_date_time_obj(course_instance.period["end_date"]) > a_actual_date and
                print("Instance:", course_instance.name)
                course_instance.execution_source_path = execution.source_path
                generate_feedback_csv(course_instance)


def generate_feedback_csv(course_instance):
    print("GFC02 - Instance:", course_instance.name)
    results = read_results(course_instance.get_result_file_name())
    feedback_list = {"LU1": [], "LU2": [], "LU3": [], "LU4": [], "LU5": []}
    for student in results.students:
        for learning_outcome in student.learning_outcomes.values():
            print("GFC05 - student, learning_outcome", student.name, learning_outcome.id )
            for feedback in learning_outcome.feedback_list:
                feedback_list[learning_outcome.id].append(feedback)
    for learning_outcome in feedback_list:
        write_feedback_csv(course_instance.get_feedback_file_name(learning_outcome), feedback_list[learning_outcome])

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

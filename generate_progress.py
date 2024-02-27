import sys
from lib.build_totals import get_overall_progress
import json
from lib.file import read_start, read_course, read_progress, read_results, read_course_instance
from lib.lib_date import get_actual_date
from lib.lib_submission import get_progress
from model.ProgressDay import ProgressDay


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(start.course_file_name)
    results = read_results(start.results_file_name)
    progress_history = read_progress(start.progress_file_name)
    progress_day = ProgressDay(results.actual_day)

    for student in results.students:
        for perspective in student.perspectives.values():
            get_progress(start, course, results, perspective)
    # bepaal de totaal voortgang
    for student in results.students:
        progress = get_overall_progress(student.perspectives)
        student.progress = progress
        progress_day.progress[str(progress)] += 1
    progress_history.append_day(progress_day)

    with open(start.results_file_name, 'w') as f:
        dict_result = results.to_json([])
        json.dump(dict_result, f, indent=2)

    with open(start.progress_file_name, 'w') as f:
        dict_result = progress_history.to_json()
        json.dump(dict_result, f, indent=2)

    print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("generate_progress.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

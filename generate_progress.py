import sys
from lib.lib_progress import get_overall_progress, get_attendance_progress, proces_progress
import json
from lib.file import read_start, read_course, read_progress, read_results, read_course_instance
from lib.lib_date import get_actual_date
from lib.lib_progress import get_progress, flow_to_progress
from model.ProgressDay import ProgressDay
from model.ProgressHistory import ProgressHistory


def generate_history(results):
    progress_history = ProgressHistory()
    for day in range(1, results.actual_day):
        new_day = ProgressDay(day)
        for student in results.students:
            progress_list = []
            for perspective in student.perspectives.values():
                progress = -1
                for submission in perspective.submissions:
                    if submission.submitted_day > day or not submission.graded:
                        break
                    else:
                        progress = flow_to_progress(submission.flow)
                new_day.perspective[perspective.name][str(progress)] += 1
                progress_list.append(progress)
            overall_progress = get_overall_progress(progress_list)
            new_day.progress[str(overall_progress)] += 1
        progress_history.append_day(new_day)
    return progress_history



def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GP02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    progress_history = read_progress(instances.get_progress_file_name(instances.current_instance))

    # progress_history = generate_history(results)
    proces_progress(start, course, results, progress_history)

    with open(instances.get_result_file_name(instances.current_instance), 'w') as f:
        dict_result = results.to_json(['perspectives'])
        json.dump(dict_result, f, indent=2)

    with open(instances.get_progress_file_name(instances.current_instance), 'w') as f:
        dict_result = progress_history.to_json()
        json.dump(dict_result, f, indent=2)

    print("GP99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GP01 - generate_progress.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

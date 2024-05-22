import sys
from canvasapi import Canvas
import json
from lib.file import read_start, read_course, read_results, read_course_instance
from lib.lib_submission import submission_builder, count_graded, add_missed_assignments, read_submissions
from lib.lib_date import API_URL, get_assignment_date, get_actual_date


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(start.course_file_name)
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    print("Canvas username:", canvas.get_current_user())
    canvas_course = canvas.get_course(start.canvas_course_id)
    results = read_results(start.results_file_name)

    if g_actual_date > start.end_date:
        results.actual_date = start.end_date
        results.actual_day = (results.actual_date - start.start_date).days
    else:
        results.actual_date = g_actual_date
        results.actual_day = (results.actual_date - start.start_date).days

    read_submissions(canvas_course, start, course, results, False)

    for student in results.students:
        for perspective in student.perspectives.values():
            add_missed_assignments(start, course, results, perspective)

    for student in results.students:
        for perspective in student.perspectives.values():
            perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_date)

    results.submission_count, results.not_graded_count = count_graded(results)

    with open(start.results_file_name, 'w') as f:
        dict_result = results.to_json(["perspectives"])
        json.dump(dict_result, f, indent=2)

    print("Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("generate_submissions.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")


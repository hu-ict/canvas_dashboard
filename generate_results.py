import sys
from canvasapi import Canvas
import json
from lib.file import read_start, read_course, read_course_instance
from lib.lib_submission import submission_builder, count_graded, add_missed_assignments, read_submissions
from model.Result import *
from lib.lib_date import get_actual_date, API_URL, get_assignment_date


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
    user = canvas.get_current_user()
    print(user.name)
    canvas_course = canvas.get_course(start.canvas_course_id)
    if g_actual_date > start.end_date:
        results = Result(start.canvas_course_id, course.name, start.end_date, (start.end_date - start.start_date).days - 1, 0, 0)
    else:
        results = Result(start.canvas_course_id, course.name, g_actual_date, (g_actual_date - start.start_date).days, 0, 0)

    results.students = course.students

    read_submissions(canvas_course, start, course, results, True)

    for student in results.students:
        for perspective in student.perspectives.values():
            # Perspective aanvullen met missed Assignments (niets ingeleverd)
            add_missed_assignments(start, course, results, perspective)

    for student in results.students:
        for perspective in student.perspectives.values():
            perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_date)

    results.submission_count, results.not_graded_count = count_graded(results)

    with open(start.results_file_name, 'w') as f:
        dict_result = results.to_json(["perspectives"])
        json.dump(dict_result, f, indent=2)

    print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    print("generate_results.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")
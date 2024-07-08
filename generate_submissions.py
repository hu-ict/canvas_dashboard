import sys
from canvasapi import Canvas
import json

from lib.file import read_start, read_course, read_results, read_course_instance, read_progress
from lib.lib_attendance import process_attendance
from lib.lib_progress import get_progress, get_overall_progress, get_attendance_progress
from lib.lib_submission import submission_builder, count_graded, add_missed_assignments, read_submissions
from lib.lib_date import API_URL, get_actual_date
from model.ProgressDay import ProgressDay


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GS02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(instances.get_course_file_name(instances.current_instance))
    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    print("GS04 - Canvas username:", canvas.get_current_user())
    canvas_course = canvas.get_course(start.canvas_course_id)
    results = read_results(instances.get_result_file_name(instances.current_instance))
    if g_actual_date > start.end_date:
        results.actual_date = start.end_date
        results.actual_day = (results.actual_date - start.start_date).days
    elif g_actual_date < start.start_date:
        results.actual_date = start.start_date
        results.actual_day = 1
    else:
        results.actual_date = g_actual_date
        results.actual_day = (results.actual_date - start.start_date).days

    read_submissions(canvas_course, start, course, results, False)

    for student in results.students:
        for perspective in student.perspectives.values():
            add_missed_assignments(start, course, results, perspective)

    if start.attendance is not None:
        process_attendance(start, course)
    else:
        print("GS06 - No attendance")

    for student in results.students:
        for perspective in student.perspectives.values():
            perspective.submissions = sorted(perspective.submissions, key=lambda s: s.assignment_day)

    results.submission_count, results.not_graded_count = count_graded(results)

    progress_history = read_progress(instances.get_progress_file_name(instances.current_instance))
    progress_day = ProgressDay(results.actual_day, course.perspectives.keys())

    for student in results.students:
        if start.attendance is not None:
            get_attendance_progress(course.attendance, results, student.attendance_perspective)
            progress_day.perspective[start.attendance.name][str(student.attendance_perspective.progress)] += 1
        for perspective in student.perspectives.values():
            get_progress(start, course, results, perspective)
            progress_day.perspective[perspective.name][str(perspective.progress)] += 1
    # bepaal de totaal voortgang
    for student in results.students:
        perspectives = []
        for perspective in student.perspectives.values():
            perspectives.append(perspective.progress)
        progress = get_overall_progress(perspectives)
        student.progress = progress
        progress_day.progress[str(progress)] += 1
    progress_history.append_day(progress_day)
    # progress_history = generate_history(results)

    with open(instances.get_progress_file_name(instances.current_instance), 'w') as f:
        dict_result = progress_history.to_json()
        json.dump(dict_result, f, indent=2)

    with open(instances.get_result_file_name(instances.current_instance), 'w') as f:
        dict_result = results.to_json(["perspectives"])
        json.dump(dict_result, f, indent=2)

    print("GS99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GS01 - generate_submissions.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")


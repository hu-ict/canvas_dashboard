import sys
from canvasapi import Canvas
import json

from generate_attendance import read_attendance
from lib.file import read_start, read_course, read_results, read_course_instance, read_progress
from lib.lib_progress import get_progress, get_overall_progress
from lib.lib_submission import submission_builder, count_graded, add_missed_assignments, read_submissions
from lib.lib_date import API_URL, get_actual_date
from model.ProgressDay import ProgressDay


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

    if len(start.attendance_perspective) > 1:
        attendances = read_attendance(start.attendance_report)
        not_found = set()
        for student in results.students:
            student.perspectives[start.attendance_perspective].submissions = []
        for attendance in attendances:
            student = results.find_student(int(attendance.student_id))
            if student:
                student.perspectives[start.attendance_perspective].submissions.append(attendance)
            else:
                not_found.add(attendance.student_id)
                # print("Student niet gevonden", attendance.student_id)
        print("Students not found", not_found)
        with open(start.results_file_name, 'w') as f:
            dict_result = results.to_json([])
            json.dump(dict_result, f, indent=2)
    else:
        print("No attendance")

    for student in results.students:
        for perspective in student.perspectives.values():
            perspective.submissions = sorted(perspective.submissions, key=lambda s: s.submitted_date)

    results.submission_count, results.not_graded_count = count_graded(results)

    progress_history = read_progress(start.progress_file_name)
    progress_day = ProgressDay(results.actual_day, course.perspectives.keys())

    for student in results.students:
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
    with open(start.results_file_name, 'w') as f:
        dict_result = results.to_json(['perspectives'])
        json.dump(dict_result, f, indent=2)

    with open(start.progress_file_name, 'w') as f:
        dict_result = progress_history.to_json()
        json.dump(dict_result, f, indent=2)

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


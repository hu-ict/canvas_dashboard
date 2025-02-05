import sys
from canvasapi import Canvas
import json

from generate_progress import proces_progress
from lib.file import read_start, read_course, read_course_instances, read_progress, read_levels_from_canvas
from lib.lib_attendance import read_attendance
from lib.lib_submission import count_graded, add_missed_assignments, read_submissions, add_open_level_moments, \
    add_open_grade_moments
from model.Result import *
from lib.lib_date import get_actual_date, API_URL, date_to_day
from model.StudentResults import StudentResults


def generate_results(instance_name):
    print("GR01 - generate_results.py")
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("GR02 - Instance:", instance.name)
    start = read_start(instance.get_start_file_name())
    course = read_course(instance.get_course_file_name())

    # Initialize a new Canvas object
    canvas = Canvas(API_URL, start.api_key)
    user = canvas.get_current_user()
    print("GR03 - Username", user.name)
    canvas_course = canvas.get_course(course.canvas_id)
    level_serie_collection = read_levels_from_canvas(canvas_course)
    if g_actual_date > course.end_date:
        results = Result(course.canvas_id, course.name, course.end_date, date_to_day(course.start_date, course.end_date), 0, 0)
    elif g_actual_date < course.start_date:
        results = Result(course.canvas_id, course.name, course.start_date, 1, 0, 0)
    else:
        results = Result(course.canvas_id, course.name, g_actual_date, date_to_day(course.start_date, g_actual_date), 0, 0)
    # for student in course.students:
    #     print("GR05 -", student.name, student.number)
    for student in course.students:
        student_results = StudentResults.copy_from(student, course)
        results.students.append(student_results)
        # with open(".//output//"+student_results.name+".json", 'w') as f:
        #     dict_results = student_results.to_json()
        #     print(student_results.name)
        #     json.dump(dict_results, f, indent=2)

    # for student in results.students:
    #     print("GR07 -", student.name, student.number)
    if course.attendance is not None:
        read_attendance(start, course, results)
    else:
        print("GR10 - No attendance")
    read_submissions(instance, canvas_course, course, results, True, level_serie_collection)
    for student in results.students:
        for student_perspective in student.perspectives.values():
            # Perspective aanvullen met missed Assignments waar nodig (niets ingeleverd)
            add_missed_assignments(instance, course, results.actual_day, student_perspective)
        add_open_level_moments(course, results.actual_day, student.id, student.student_level_moments)
        add_open_grade_moments(course, results.actual_day, student.id, student.student_grade_moments)
    # for student in results.students:
    #     print("GR75", student.name)
    # sorteer de attendance en submissions
    for student in results.students:
        if course.attendance is not None:
            student.student_attendance.attendance_submissions = sorted(student.student_attendance.attendance_submissions, key=lambda s: s.day)
        for perspective in student.perspectives.values():
            for submission_sequence in perspective.submission_sequences:
                submission_sequence.submissions = sorted(submission_sequence.submissions, key=lambda s: s.assignment_day)
            perspective.submission_sequences = sorted(perspective.submission_sequences, key=lambda s: s.get_day())

    results.submission_count, results.not_graded_count = count_graded(results)

    # with open(instances.get_result_file_name(instances.current_instance), 'w') as f:
    #     dict_result = results.to_json(["perspectives"])
    #     json.dump(dict_result, f, indent=2)
    progress_history = read_progress(instance.get_progress_file_name())
    proces_progress(course, results, progress_history)
    # progress_history = generate_history(results)

    with open(instance.get_progress_file_name(), 'w') as f:
        dict_result = progress_history.to_json()
        json.dump(dict_result, f, indent=2)

    for student in results.students:
        # print(l_peil_construction)
        print("GR41 -", student.name)
        student_name = student.email.split("@")[0].lower()
        file_name_json = instance.get_student_path() + student_name + ".json"
        with open(file_name_json, 'w') as f:
            dict_result = student.to_json()
            json.dump(dict_result, f, indent=2)

    with open(instance.get_result_file_name(), 'w') as f:
        dict_result = results.to_json()
        json.dump(dict_result, f, indent=2)

    print("GR99 Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_results(sys.argv[1])
    else:
        generate_results("")
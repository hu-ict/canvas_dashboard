# Haalt de studenten en de projecten op. Maakt een JSON waarin de url's naar de daily wordt opgeslagen.
import csv

from canvasapi import Canvas
import json

from lib.build_totals import get_actual_progress
from lib.file import read_start, read_course, read_progress, read_results
from lib.lib_submission import submission_builder, NO_SUBMISSION, remove_assignment, bepaal_voortgang, count_graded
from model.Comment import Comment
from model.ProgressDay import ProgressDay
from model.Result import *
from lib.lib_date import get_actual_date, API_URL, get_assignment_date, date_to_day, get_date_time_obj_loc
from model.Submission import Submission

def read_attendance(attendance_file_name):
    print("read_attendance", attendance_file_name)
    appendances = []
    with open(attendance_file_name, mode='r', encoding="utf-8") as attendance_file:
        DictReader_obj = csv.DictReader(attendance_file, delimiter=";")
        for item in DictReader_obj:
            if item["Attendance"] == "present":
                score = 2
            elif item["Attendance"] == "absent":
                score = 0
            else:
                score = 1
            l_date = get_date_time_obj_loc(item["Class Date"])
            l_submission = Submission(0, 72500, 0, item["Student ID"], "Attendance", l_date, l_date, True, score, 2)
            appendances.append(l_submission)
    return appendances


g_actual_date = get_actual_date()
start = read_start()
if start.attendance_report is not None:
    course = read_course(start.course_file_name)
    results = read_results(start.results_file_name)
    results.actual_date = g_actual_date
    g_actual_day = (results.actual_date - start.start_date).days
    attendances = read_attendance(start.attendance_report)
    not_found = set()
    for student in results.students:
        student.perspectives["aanwezig"].submissions = []
    for attendance in attendances:
        student = results.find_student(int(attendance.student_id))
        if student:
            student.perspectives["aanwezig"].submissions.append(attendance)
        else:
            not_found.add(attendance.student_id)
            # print("Student niet gevonden", attendance.student_id)

    print("Students not found", not_found)
    with open(start.results_file_name, 'w') as f:
        dict_result = results.to_json([])
        json.dump(dict_result, f, indent=2)
else:
    print("No attendance")

# with open(start.progress_file_name, 'w') as f:
#     dict_result = progress_history.to_json()
#     json.dump(dict_result, f, indent=2)

print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")
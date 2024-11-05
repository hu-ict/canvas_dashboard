import csv

from lib.lib_date import get_date_time_obj_alt, date_to_day
from model.Submission import Submission
from model.perspective.AttendanceSubmission import AttendanceSubmission


def read_attendance_from_file(start, course):
    print("read_attendance", start.attendance_report)
    appendances = []
    with open(start.attendance_report, mode='r', encoding="utf-8") as attendance_file:
        DictReader_obj = csv.DictReader(attendance_file, delimiter=",")
        for item in DictReader_obj:
            if item["Attendance"] == "present":
                score = 2
            elif item["Attendance"] == "late":
                score = 1
            elif item["Attendance"] == "absent":
                score = 0
            else:
                score = -1
            if "Geldige reden" in item:
                if item["Geldige reden"] == "Geldige reden" and score < 2:
                    score += 1
            l_date = get_date_time_obj_alt(item["Class Date"])
            l_teacher_id = item["Teacher ID"]
            l_teacher_name = item["Teacher Name"]
            l_day = date_to_day(course.start_date, l_date)
            attendance_submission = AttendanceSubmission("Attendance", int(item["Student ID"]), l_date, l_day, l_teacher_name, score, 2, 0)
            if attendance_submission.student_id == 994:
                print("LA05 -", attendance_submission)
            appendances.append(attendance_submission)
    return appendances


def read_attendance(start, course, results):
    attendances = read_attendance_from_file(start, course)
    not_found = set()
    for student in results.students:
        student.student_attendance.attendance_submissions = []
    for attendance in attendances:
        student = results.find_student(attendance.student_id)
        if student:
            student.student_attendance.attendance_submissions.append(attendance)
        else:
            not_found.add(attendance.student_id)
            # print("Student niet gevonden", attendance.student_id)
    print("LA03 - Students not found", not_found)

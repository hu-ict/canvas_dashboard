import csv

from lib.lib_date import get_date_time_obj_alt, date_to_day
from model.Submission import Submission


def read_attendance(start):
    print("read_attendance", start.attendance_report)
    appendances = []
    with open(start.attendance_report, mode='r', encoding="utf-8") as attendance_file:
        DictReader_obj = csv.DictReader(attendance_file, delimiter=",")
        for item in DictReader_obj:
            if item["Attendance"] == "present":
                score = 2
            elif item["Attendance"] == "absent":
                score = 0
            else:
                score = 1
            l_date = get_date_time_obj_alt(item["Class Date"])
            l_day = date_to_day(start.start_date, l_date),
            l_submission = Submission(0, 72500, 0, int(item["Student ID"]), "Attendance", l_date, l_day, l_date, l_day, True, "Attendance", l_date, score, 2, 0)
            appendances.append(l_submission)
    return appendances


def process_attendance(start, results):
    attendances = read_attendance(start)
    not_found = set()
    for student in results.students:
        student.attendance.submissions = []
    for attendance in attendances:
        student = results.find_student(int(attendance.student_id))
        if student:
            student.attendance.submissions.append(attendance)
        else:
            not_found.add(attendance.student_id)
            # print("Student niet gevonden", attendance.student_id)
    print("LA03 - Students not found", not_found)

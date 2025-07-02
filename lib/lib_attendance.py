import csv

from lib.lib_date import get_date_time_obj_alt, date_to_day
from model.Submission import Submission
from model.perspective.AttendanceSubmission import AttendanceSubmission


def read_attendance_from_file(start, course):
    print("read_attendance", start.attendance_report)
    attendances = []
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
            l_grade = str(score)
            l_value = score
            attendance_submission = AttendanceSubmission("Attendance", int(item["Student ID"]), l_date, l_day, l_teacher_name, l_grade, score, l_value, 2, 0)
            attendances.append(attendance_submission)
    return attendances


def get_attendance_progress(attendance, student):
    # bepaal de voortgang
    student.student_attendance.attendance_submissions = sorted(student.student_attendance.attendance_submissions, key=lambda s: s.day)
    student.student_attendance.count = 0
    student.student_attendance.percentage = 0
    student.student_attendance.essential_count = 0
    student.student_attendance.essential_percentage = 0.0
    essential_score = 0
    essential_total_points = 0
    total_points = 0
    last_flow = 1.0
    for submission in student.student_attendance.attendance_submissions:
        moment = attendance.get_moment(submission.day)
        student.student_attendance.count += 1
        total_points += submission.score
        student.student_attendance.percentage = total_points / student.student_attendance.count / 2
        if moment is not None:
            # print("LP61 -", moment)
            # alleen op vastgestelde dagen wordt aanwezigheid beloond
            essential_score += submission.score
            essential_total_points += submission.points
            student.student_attendance.essential_count += 1
            student.student_attendance.essential_percentage = essential_score / essential_total_points
            submission.flow = round(student.student_attendance.essential_percentage, 3)
            last_flow = submission.flow
            if "1885886" == student.number:
                print("GAP03 -",submission.day, submission.score, essential_score, essential_total_points, submission.flow)
        else:
            submission.flow = last_flow
        student.student_attendance.last_score = submission.day
    if student.student_attendance.essential_count == 0:
        # Niet te bepalen
        return 0
    elif student.student_attendance.last_score != 0:
        # print(f"LP54 - Laatste dag {attendance_perspective.last_score}, laatste waarde {attendance_perspective.sum_score}")
        return attendance.bandwidth.get_progress(student.student_attendance.last_score,  student.student_attendance.essential_percentage*100)
        # print(f"LP55 - Laatste dag {attendance_perspective.last_score}, laatste waarde {attendance_perspective.sum_score*100}, voortgang {attendance_perspective.progress}")
    else:
        # Niet te bepalen
        return 0


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

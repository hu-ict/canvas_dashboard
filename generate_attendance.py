# Haalt de studenten en de projecten op. Maakt een JSON waarin de url's naar de daily wordt opgeslagen.
import csv
import sys

from canvasapi import Canvas
import json

from lib.file import read_start, read_course, read_results, read_course_instance
from lib.lib_plotly import attendance_to_level

from lib.lib_date import get_actual_date, get_date_time_obj_alt
from model.Submission import Submission

def read_attendance(attendance_file_name):
    print("read_attendance", attendance_file_name)
    appendances = []
    with open(attendance_file_name, mode='r', encoding="utf-8") as attendance_file:
        DictReader_obj = csv.DictReader(attendance_file, delimiter=",")
        for item in DictReader_obj:
            if item["Attendance"] == "present":
                score = 2
            elif item["Attendance"] == "absent":
                score = 0
            else:
                score = 1
            l_date = get_date_time_obj_alt(item["Class Date"])
            l_submission = Submission(0, 72500, 0, item["Student ID"], "Attendance", l_date, l_date, True, score, 2, 0)
            appendances.append(l_submission)
    return appendances

def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    if start.attendance_report is not None:
        course = read_course(start.course_file_name)
        results = read_results(start.results_file_name)
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
        for student in results.students:
            for perspective in student.perspectives.values():
                if perspective.name == "aanwezig":
                    flow_total = 0
                    flow_count = 0
                    for submission in perspective.submissions:
                        flow_total += submission.score
                        flow_count += 1
                        submission.flow = flow_total / flow_count * 100 / 2
                    perspective.progress = attendance_to_level(submission.flow/100)

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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

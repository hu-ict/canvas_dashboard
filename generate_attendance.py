import csv
import sys
import json
from lib.file import read_start, read_results, read_course_instances, read_course
from lib.lib_attendance import read_attendance
from lib.lib_date import get_actual_date
from lib.lib_progress import get_attendance_progress


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    instance = instances.get_instance_by_name(instances.current_instance)
    print("GCS02 -", "Instance:", instance.name)
    start = read_start(instance.get_start_file_name())
    course = read_course(instance.get_course_file_name())
    results = read_results(instance.get_result_file_name())
    if course.attendance is not None:
        read_attendance(start, course, results)
        for student in results.students:
            get_attendance_progress(course.attendance, student)
    else:
        print("GA10 - No attendance")
    with open(instance.get_result_file_name(), 'w') as f:
        dict_result = results.to_json()
        json.dump(dict_result, f, indent=2)

    print("GA99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    print("GR01 - generate_attendance.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

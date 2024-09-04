import csv
import sys
import json
from lib.file import read_start, read_results, read_course_instance, read_course
from lib.lib_attendance import process_attendance
from lib.lib_date import get_actual_date


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GA02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(instances.get_course_file_name(instances.current_instance))
    results = read_results(instances.get_result_file_name(instances.current_instance))
    if start.attendance is not None:
        process_attendance(start, course, results)
    else:
        print("GA04 - No attendance")

    with open(instances.get_result_file_name(instances.current_instance), 'w') as f:
        dict_result = results.to_json(["perspectives"])
        json.dump(dict_result, f, indent=2)

    print("GA99 Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    print("GR01 - generate_attendance.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

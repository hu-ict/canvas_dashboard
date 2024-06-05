import csv
import sys
import json
from lib.file import read_start, read_results, read_course_instance
from lib.lib_attendance import read_attendance, process_attendance
from lib.lib_date import get_actual_date


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    results = read_results(start.results_file_name)
    if start.attendance is not None:
        process_attendance(start, results)
    else:
        print("No attendance")

    print("Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

import json
import sys
from lib.file import read_start, read_course, read_progress, read_results, read_course_instance
from lib.lib_bandwidth import bandwidth_builder, bandwidth_builder_attendance
from lib.lib_date import get_actual_date

def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GB02 - Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    course = read_course(instances.get_course_file_name(instances.current_instance))
    for assignment_group in course.assignment_groups:
        if assignment_group.strategy == "NONE":
            assignment_group.bandwidth = None
        else:
            assignment_group.bandwidth = bandwidth_builder(assignment_group, course.days_in_semester)
    if course.attendance is not None:
        course.attendance.bandwidth = bandwidth_builder_attendance(course.attendance.lower_points, course.attendance.upper_points, course.attendance.total_points, course.days_in_semester)
    with open(instances.get_course_file_name(instances.current_instance), 'w') as f:
        dict_result = course.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)
    print("GB99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GB01 - generate_bandwidth.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

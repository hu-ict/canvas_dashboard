import json
import sys
from lib.file import read_start, read_course, read_course_instances
from lib.lib_bandwidth import bandwidth_builder, bandwidth_builder_attendance
from lib.lib_date import get_actual_date

def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("GB02 - Instance:", instances.current_instance)
    instance = instances.get_instance_by_name(instances.current_instance)
    course = read_course(instance.get_course_file_name())
    for assignment_group in course.assignment_groups:
        assignment_group.assignment_sequences = sorted(assignment_group.assignment_sequences, key=lambda a: a.get_day())
        assignment_group.bandwidth = bandwidth_builder(assignment_group, course.days_in_semester)
    if course.attendance is not None:
        course.attendance.bandwidth = bandwidth_builder_attendance(course.attendance.lower_points, course.attendance.upper_points, course.attendance.total_points, course.days_in_semester)
    with open(instance.get_course_file_name(), 'w') as f:
        dict_result = course.to_json()
        json.dump(dict_result, f, indent=2)
    print("GB99 - Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    print("GB01 - generate_bandwidth.py")
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

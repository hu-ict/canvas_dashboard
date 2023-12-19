import json
import sys
from lib.file import read_start, read_course, read_progress, read_results, read_course_instance
from lib.lib_bandwidth import bandwidth_builder
from lib.lib_date import get_actual_date

def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    start = read_start(instances.get_start_file_name())
    config = read_course(start.course_file_name)

    for assignment_group in config.assignment_groups:
        assignment_group.assignments = sorted(assignment_group.assignments, key=lambda a: a.assignment_day)

        if assignment_group.strategy == "NONE":
            assignment_group.bandwidth = None
        else:
            assignment_group.bandwidth = bandwidth_builder(assignment_group, config.days_in_semester)

    with open(start.course_file_name, 'w') as f:
        dict_result = config.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)

    print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

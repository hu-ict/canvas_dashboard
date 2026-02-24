import sys

from scripts.env_2.generate_course import generate_course
from scripts.lib.file import read_environment
from scripts.lib.lib_date import get_actual_date, get_date_time_obj
from scripts.env_2.generate_results import generate_results
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME


def run_env_2(a_actual_date):
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    execution = environment.get_execution_by_name("env_2")
    # loopt alle courses af in de environment.json
    for course in environment.courses:
        print("RUN211- course.name", course.name)
        # loopt alle course_instances af in de environment.json
        for course_instance in course.course_instances:
            print("RUN212 - course_instance", course_instance.name)
            if course_instance.stage != "SLEEP": #get_date_time_obj(course_instance.period["end_date"]) > a_actual_date and
                print("RUN213 - Instance:", course_instance.name)
                course_instance.execution_source_path = execution.source_path
                generate_course(course_instance)
                generate_results(course_instance)


if __name__ == "__main__":
    l_actual_date = get_actual_date()
    sys.stdout.reconfigure(encoding="utf-8")
    run_env_2(l_actual_date)
    total_seconds = (get_actual_date() - l_actual_date).seconds
    seconds = total_seconds % 60
    minutes = total_seconds // 60
    print(f"Time running: {minutes}:{seconds:02d} (m:ss)")
    print("Time running:", total_seconds, "seconds")
    print("Date running:", get_actual_date())

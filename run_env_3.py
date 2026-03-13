import sys

from scripts.env_3.generate_user_data import generate_user_data
from scripts.lib.file import read_environment
from scripts.lib.lib_date import get_actual_date, get_date_time_obj
from scripts.env_3.generate_dashboard import generate_dashboard
from scripts.env_3.generate_plotly import generate_plotly
from scripts.env_3.generate_portfolio import generate_portfolio
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME
from scripts.publish_dashboard import publish_dashboard


def run_env_3(a_actual_date):
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    execution = environment.get_execution_by_name("env_3")
    for course in environment.courses:
        for course_instance in course.course_instances:
            if course_instance.stage != "SLEEP": #get_date_time_obj(course_instance.period["end_date"]) > a_actual_date and
                print("Instance:", course_instance.name)
                course_instance.execution_source_path = execution.source_path
                generate_dashboard(course_instance)
                generate_plotly(course_instance)
                generate_portfolio(course_instance)
                publish_dashboard(course_instance)
                # generate_user_data(course_instance)


if __name__ == "__main__":
    l_actual_date = get_actual_date()
    sys.stdout.reconfigure(encoding="utf-8")
    run_env_3(l_actual_date)
    total_seconds = (get_actual_date() - l_actual_date).seconds
    seconds = total_seconds % 60
    minutes = total_seconds // 60
    print(f"Time running: {minutes}:{seconds:02d} (m:ss)")
    print("Time running:", total_seconds, "seconds")
    print("Date running:", get_actual_date())

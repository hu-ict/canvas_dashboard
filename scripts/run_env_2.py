from scripts.lib.file import read_environment, read_workflow
from lib.lib_date import get_actual_date, get_date_time_obj
from scripts.env_2.generate_course import generate_course
from scripts.env_3.generate_dashboard import generate_dashboard
from scripts.env_3.generate_plotly import generate_plotly
from scripts.env_3.generate_portfolio import generate_portfolio
from scripts.env_2.generate_results import generate_results
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, WORKFLOW_FILE_NAME
from scripts.publish_dashboard import publish_dashboard


def main():
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    event = "env-2_results_create_event"
    execution = environment.get_execution_by_name("env_2")
    for course in environment.courses:
        for course_instance in course.course_instances:
            if get_date_time_obj(course_instance.period["end_date"]) > l_actual_date:
                print("R2E04 - Instance:", course_instance.name, event)
                course_instance.execution_source_path = execution.source_path
                workflow = read_workflow(WORKFLOW_FILE_NAME)
                action = workflow.get_action_by_name(event)
                for python_script in action.run:
                    print("R2E05 - Event", action.name, "course_code", course.name, "course_instance", course_instance.name +":>", python_script)
                    if python_script == "generate_course.py":
                        generate_course(course.name, course_instance.name)
                    elif python_script == "generate_results.py":
                        generate_results(course.name, course_instance.name)
                    elif python_script == "generate_dashboard.py":
                        generate_dashboard(course.name, course_instance.name)
                    elif python_script == "generate_plotly.py":
                        generate_plotly(course.name, course_instance.name)
                    elif python_script == "generate_portfolio.py":
                        generate_portfolio(course.name, course_instance.name)
                    elif python_script == "publish_dashboard.py":
                        publish_dashboard(course.name, course_instance.name)
                    else:
                        print("R2E07 - Script wordt niet herkend.", python_script)

    print("R2E11 -", event)


if __name__ == "__main__":
    l_actual_date = get_actual_date()
    main()
    total_seconds = (get_actual_date() - l_actual_date).seconds
    seconds = total_seconds % 60
    minutes = total_seconds // 60
    print(f"Time running: {minutes}:{seconds:02d} (m:ss)")
    print("Time running:", total_seconds, "seconds")
    print("Date running:", get_actual_date())

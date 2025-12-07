import json
import sys

from scripts.lib.file import read_environment, read_workflow
from lib.lib_date import get_actual_date
from scripts.env_2.generate_course import generate_course
from scripts.env_3.generate_dashboard import generate_dashboard
from scripts.env_3.generate_plotly import generate_plotly
from scripts.env_3.generate_portfolio import generate_portfolio
from scripts.env_2.generate_results import generate_results
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, WORKFLOW_FILE_NAME
from scripts.publish_dashboard import publish_dashboard


def main(course_code, instance_name, event):
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    if course_instance is None:
        print("RUN31 - ERROR course_instance not found in environment.json", instance_name)
        return
    print("Instance:", course_instance.name)
    workflow = read_workflow(WORKFLOW_FILE_NAME)
    action = workflow.get_action_by_name(event)
    for python_script in action.run:
        print("OP05 - Event", action.name, "course_code", course_code, "course_instance", instance_name +":>", python_script)
        if python_script == "generate_course.py":
            generate_course(course_code, instance_name)
        elif python_script == "generate_results.py":
            generate_results(course_code, instance_name)
        elif python_script == "generate_dashboard.py":
            generate_dashboard(course_code, instance_name)
        elif python_script == "generate_plotly.py":
            generate_plotly(course_code, instance_name)
        elif python_script == "generate_portfolio.py":
            generate_portfolio(course_code, instance_name)
        elif python_script == "publish_dashboard.py":
            publish_dashboard(course_code, instance_name)
        else:
            print("OP51 - Script wordt niet herkend.", python_script)

    print("RUN11 -", event)


if __name__ == "__main__":
    l_actual_date = get_actual_date()
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        pass
        # main("TICT-V1SE1-24-SEP2025", "course_create_event")
        # main("TICT-V3SE5-25_SEP25", "course_create_event")
        # main("TICT-V3SE6-25", "TICT-V3SE6-25_sep25", "course_create_event")
        # main("TICT-V3SE6-25", "TICT-V3SE6-25_sep25_test", "results_create_event")
    total_seconds = (get_actual_date() - l_actual_date).seconds
    seconds = total_seconds % 60
    minutes = total_seconds // 60

    print(f"Time running: {minutes}:{seconds:02d} (m:ss)")
    print("Time running:", total_seconds, "seconds")
    print("Date running:", get_actual_date())

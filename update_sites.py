import json
import sys

from lib.file import read_course, read_msteams_api, read_course_instances, read_environment
from lib.lib_date import get_actual_date
from lib.teams_api_lib import teams, get_channels, get_drive, get_me_for_check, get_access_token
from model.TeamsApi import Channel
from model.environment.Environment import ENVIRONMENT_FILE_NAME


def update_sites(course_code, instance_name):
    print("GCS01 - generate_results.py")
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    if len(instance_name) > 0:
        environment.current_instance = {"course_name": course_code, "course_instance_name": instance_name}
        with open(ENVIRONMENT_FILE_NAME, 'w') as f:
            dict_result = environment.to_json()
            json.dump(dict_result, f, indent=2)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    print("Instance:", course_instance.name)

    if course_instance.course_code not in ["TICT-VINNO1-22", "TICT-V3SE6-25"]:
        print("US04 - No student channels defined for this course")
        return
    course = read_course(course_instance.get_course_file_name())
    msteams_api = read_msteams_api("msteams_api.json")
    if get_me_for_check(msteams_api.gen_token) is None:
        token = get_access_token(msteams_api.tenant_id, msteams_api.client_id)
        print(token)
        msteams_api.gen_token = token
        with open("msteams_api.json", 'w') as f:
            dict_result = msteams_api.to_json()
            json.dump(dict_result, f, indent=2)

    # student_sites = get_sites(msteams_api.my_token, "Sep24")
    channel_count = 0
    site_count = 0
    for team_id in teams:
        # team = get_team(msteams_api.my_token, team_id)
        # print("US05 -", team)
        student_channels = get_channels(msteams_api.gen_token, team_id)
        channel_count += len(student_channels)
        for channel in student_channels:
            student = course.find_student_by_email_part(channel["display_name"])
            if student is None:
                print(f"US06 - Student not found in course: [{channel['display_name']}]")
            else:
                print("US07 - Student", student.name)
                drive = get_drive(msteams_api.gen_token, team_id, channel["id"])
                # print("US81 - Drive", drive)
                site_count += 1
                student.site = drive["drive_id"]
                msteams_api.channels.append(Channel(student.id, student.name, drive["drive_id"]))
    print("US10 - Channels:", channel_count, "Students linked:", site_count)
    sites = 0
    errors = 0
    for student in course.students:
        if len(student.site) == 0:
            print("US12 - No channel in teams, display_name:", student.name)
            errors += 1
        else:
            # print("US13 - displayName:", student.name)
            sites += 1
    print("US15 - Sites", sites, "Errors", errors)

    with open("msteams_api.json", 'w') as f:
        dict_result = msteams_api.to_json()
        json.dump(dict_result, f, indent=2)

    with open(course_instance.get_course_file_name(), 'w') as f:
        dict_result = course.to_json()
        json.dump(dict_result, f, indent=2)

    print("US99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_sites(sys.argv[1], sys.argv[2])
    else:
        update_sites("", "")

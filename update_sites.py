import json
import sys

from scripts.lib.file import read_course, read_msteams_api, read_environment
from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, MSTEAMS_API_KEY_FILE_NAME
from scripts.lib.lib_date import get_actual_date
from scripts.lib.teams_api_lib import teams, get_channels, get_drive, get_me_for_check, get_access_token, \
    get_team
from scripts.model.TeamsApi import Channel


def update_sites(course_code, instance_name):
    print("UPS01 - update_sites.py", instance_name)
    g_actual_date = get_actual_date()
    environment = read_environment(ENVIRONMENT_FILE_NAME)
    environment.current_instance["course_name"] = course_code
    environment.current_instance["course_instance_name"] = instance_name
    current_instance = environment.get_instance_of_course(environment.current_instance)
    print("UPS02 - Instance:", current_instance.name)
    course_instance = environment.get_instance_of_course(environment.current_instance)
    if course_instance.course_code not in ["TICT-V3SE6-25"]:
        print("US04 - No student channels defined for this course")
        return
    course = read_course(course_instance.get_course_file_name())
    msteams_api = read_msteams_api(MSTEAMS_API_KEY_FILE_NAME)
    token = msteams_api.gen_token
    print(token)
    if get_me_for_check(token) is None:
        token = get_access_token(msteams_api.tenant_id, msteams_api.client_id)
        print(token)
        msteams_api.gen_token = token
        print(msteams_api.gen_token)
        with open(MSTEAMS_API_KEY_FILE_NAME, 'w') as f:
            dict_result = msteams_api.to_json()
            json.dump(dict_result, f, indent=2)

    # student_sites = get_sites(msteams_api.my_token, "Sep24")
    channel_count = 0
    site_count = 0
    team_index = 0
    team_files = ["team_1.json", "team_2.json", "team_3.json", "team_4.json", "team_5.json"]
    msteams_api.channels = []  # opschonen van de lijst
    for team in teams:
        team_id = team #teams[team_index]
        team = get_team(token, team_id)
        print("UPS05 -", team)
        student_channels = get_channels(token, team_id)
        # student_channels = get_channels_from_json(team_file)
        channel_count += len(student_channels)
        for channel in student_channels:
            print(channel)
            student = course.find_student_by_email_part(channel["display_name"])
            if student is None:
                print(f"UPS06 - Student not found in course: [{channel['display_name']}]")
            else:
                print("UPS07 - Student", student.email)
                drive = get_drive(token, team_id, channel["id"])
                # print("US81 - Drive", drive)
                site_count += 1
                student.site = drive["drive_id"]
                msteams_api.channels.append(Channel(student.id, student.name, drive["drive_id"]))
        team_index += 1
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

    with open(MSTEAMS_API_KEY_FILE_NAME, 'w') as f:
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
        update_sites("TICT-V3SE6-25", "TICT-V3SE6-25_feb26")

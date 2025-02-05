import json
import sys

from lib.file import read_course, read_msteams_api, read_course_instances
from lib.lib_date import get_actual_date
from lib.teams_api_lib import teams, get_channels, get_drive, get_me_for_check, get_access_token
from model.TeamsApi import Channel


def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instances()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    instance = instances.get_instance_by_name(instances.current_instance)
    print("PB02 - Instance:", instance.name)

    if instances.current_instance != "sep24_inno":
        print("US04 - No student channels defined for this course")
        return
    course = read_course(instance.get_course_file_name())
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
            student = course.find_student_by_name(channel["display_name"])
            if student is None:
                print(f"US06 - Student not found in course: [{channel['display_name']}]")
            else:
                drive = get_drive(msteams_api.gen_token, team_id, channel["id"])
                print("US81 - Drive", drive)
                site_count += 1
                student.site = drive["drive_id"]
                msteams_api.channels.append(Channel(student.id, student.name, drive["drive_id"]))
    print("US10 - Channels:", channel_count, "Students linked:", site_count)

    for student in course.students:
        if student.site == "":
            print("US12 - No channel in teams, display_name:", student.name)
        # else:
        #     print("US13 - displayName:", student.name)

    with open("msteams_api.json", 'w') as f:
        dict_result = msteams_api.to_json()
        json.dump(dict_result, f, indent=2)

    with open(instance.get_course_file_name(), 'w') as f:
        dict_result = course.to_json()
        json.dump(dict_result, f, indent=2)

    print("US99 - Time running:", (get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

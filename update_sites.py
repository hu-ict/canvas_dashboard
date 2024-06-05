import json
import sys

from lib.file import read_start, read_course, read_msteams_api, read_course_instance
from lib.lib_date import get_actual_date
from lib.teams_api_lib import get_sites, get_me_for_check, get_access_token, teams, get_channels, get_team

instances = read_course_instance()
print("Instance:", instances.current_instance)
start = read_start(instances.get_start_file_name())
course = read_course(start.course_file_name)
msteams_api = read_msteams_api("msteams_api.json")

# if get_me_for_check(msteams_api.gen_token) is None:
#     print("Obtain new token")
#     token = get_access_token(msteams_api.tenant_id, msteams_api.client_id)
#     print(token)
#     msteams_api.gen_token = token
#     with open("msteams_api.json", 'w') as f:
#         dict_result = msteams_api.to_json()
#         json.dump(dict_result, f, indent=2)

def main(instance_name):
    g_actual_date = get_actual_date()
    instances = read_course_instance()
    if len(instance_name) > 0:
        instances.current_instance = instance_name
    print("Instance:", instances.current_instance)
    if instances.current_instance != "feb24_inno":
        print("No student channels defined for this course")
        return

    student_sites = get_sites(msteams_api.my_token, "Feb24")
    channel_count = 0
    for team_id in teams:
        team = get_team(msteams_api.my_token, team_id)
        print(team)
        student_channels = get_channels(msteams_api.my_token, team_id)
        channel_count += len(student_channels)
        for channel in student_channels:
            if channel in student_sites.keys():
                print("Has site:", channel)
                print(student_sites[channel])
            else:
                print("Has NO site", channel)
    print("Channels:", channel_count, "Sites:", len(student_sites))


    for student in course.students:
        if student.name in student_sites.keys():
            print("displayName:", student.name)
            student.site = student_sites[student.name]
        else:
            print("Student from channel name not found", student.name)

    with open(start.course_file_name, 'w') as f:
        dict_result = course.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)

    print("Time running:",(get_actual_date() - g_actual_date).seconds, "seconds")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("")

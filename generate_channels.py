import json
from lib.file import read_start, read_course, read_msteams_api, read_course_instance
from lib.teams_api_lib import get_team_channels, get_me_for_check, get_access_token, add_member_to_team, \
    add_member_to_channel, create_channel

# teams like ["b7cf78ae-8c6f-460d-a47a-d4bc2b8b2f18"]
teams = []

RedirectURI = "https://localhost"

instances = read_course_instance()
start = read_start(instances.get_start_file_name())
course = read_course(start.course_file_name)
msteams_api = read_msteams_api("msteams_api.json")

if get_me_for_check(msteams_api.gen_token) is None:
    token = get_access_token(msteams_api.tenant_id, msteams_api.client_id)
    print(token)
    msteams_api.gen_token = token
    with open("msteams_api.json", 'w') as f:
        dict_result = msteams_api.to_json()
        json.dump(dict_result, f, indent=2)

print(len(course.students))
student_count = 1
for student in course.students:
    team_id = teams[student_count % len(teams)]
    print(team_id, student.email)
    channel_id = create_channel(msteams_api.gen_token, team_id, student.name)
    if channel_id:
        print(channel_id, student.email)
        add_member_to_team(msteams_api.gen_token, team_id, student.email)
        add_member_to_channel(msteams_api.gen_token, team_id, channel_id, student.email)
    student_count += 1

with open(start.course_file_name, 'w') as f:
    dict_result = course.to_json(["assignment"])
    json.dump(dict_result, f, indent=2)


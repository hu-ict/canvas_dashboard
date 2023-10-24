import json
from lib.file import read_start, read_course, read_msteams_api
from lib.teams_api_lib import get_team_channels, get_me_for_check, get_access_token, add_member_to_team, add_member_to_channel
RedirectURI = "https://localhost"

g_team_ids = ["b7cf78ae-8c6f-460d-a47a-d4bc2b8b2f18", "2d570ef0-7a51-489e-a2e3-681440e67d08", "82e424d3-5baa-4ba2-b2f8-85b3659a150e", "a282ec15-7540-4c3b-bb3c-26b2f38377c7"]
start = read_start()
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
for l_team_id in g_team_ids:
    l_channels = get_team_channels(msteams_api.gen_token, l_team_id)
    for l_channel in l_channels:
        l_channel_id = l_channels[l_channel]
        l_student = course.find_student_by_name(l_channel)
        if l_student is not None:
            print(l_team_id, l_student.email)
            add_member_to_team(msteams_api.gen_token, l_team_id, l_student.email)
            print(l_channel_id, l_student.email)
            add_member_to_channel(msteams_api.gen_token, l_team_id, l_channel_id, l_student.email)
        else:
            print("Student not found:", l_channel)

with open(start.course_file_name, 'w') as f:
    dict_result = course.to_json(["assignment"])
    json.dump(dict_result, f, indent=2)


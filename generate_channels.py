import json
from lib.file import read_start, read_course, read_msteams_api, read_course_instance
from lib.teams_api_lib import get_team_channels, get_me_for_check, get_access_token, add_member_to_team, \
    add_member_to_channel, create_channel

# teams like ["b7cf78ae-8c6f-460d-a47a-d4bc2b8b2f18"]
teams = []

RedirectURI = "https://localhost"

instances = read_course_instance()
print("GC02 -", "Instance:", instances.current_instance)
start = read_start(instances.get_start_file_name())
course = read_course(instances.get_course_file_name(instances.current_instance))
msteams_api = read_msteams_api("msteams_api.json")

if get_me_for_check(msteams_api.gen_token) is None:
    token = get_access_token(msteams_api.tenant_id, msteams_api.client_id)
    print(token)
    msteams_api.gen_token = token
    with open("msteams_api.json", 'w') as f:
        dict_result = msteams_api.to_json()
        json.dump(dict_result, f, indent=2)

print(f"Aantal studenten {len(course.students)}, aantal teams {len(teams)}")
student_count = 1
if len(teams) > 0:
    for student in course.students:
        team_id = teams[student_count % len(teams)]
        print(team_id, student.email)
        channel_id = create_channel(msteams_api.gen_token, team_id, student.name)
        if channel_id:
            print(channel_id, student.email)
            add_member_to_team(msteams_api.gen_token, team_id, student.email)
            add_member_to_channel(msteams_api.gen_token, team_id, channel_id, student.email)
        student_count += 1

    teams = {"TICT-ICT-V1A-24-TEST": {'id': "b7cf78ae-8c6f-460d-a47a-d4bc2b8b2f18"}}

    for group in course.student_groups:
        if len(group.students) > 30:
            print("GC11 - ERROR - Te veel studenten in de groep (", group.name, "). Maximaal 30 studenten, gevonden", len(group.students), "studenten")
        else:
            print("GC12 - Voor groep (", group.name, ")", len(group.students), "studenten gevonden")
            for student_link in group.students:
                student = course.find_student(student_link.id)
                if student is not None:
                    team = teams[group.name].values()
                    team_id = team['id']
                    channel_id = create_channel(msteams_api.gen_token, team_id, student.name)
                    if channel_id:
                        print(channel_id, student.email)
                        add_member_to_team(msteams_api.gen_token, team_id, student.email)
                        add_member_to_channel(msteams_api.gen_token, team_id, channel_id, student.email)
                    student_count += 1

    with open(start.course_file_name, 'w') as f:
        dict_result = course.to_json(["assignment"])
        json.dump(dict_result, f, indent=2)


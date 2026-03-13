import json

from scripts.lib.file import read_environment, read_course, read_msteams_api
from scripts.lib.file_const import MSTEAMS_API_KEY_FILE_NAME, ENVIRONMENT_FILE_NAME
from scripts.lib.teams_api_lib import get_me_for_check, get_access_token, get_team, create_channel, add_member_to_team, \
    add_member_to_channel, teams

print("GCH01 - generate_channels.py")
RedirectURI = "https://localhost"

environment = read_environment(ENVIRONMENT_FILE_NAME)
execution = environment.get_execution_by_name("env_2")
course_instance = environment.get_current_instance()
print("RUN213 - Instance:", course_instance.name)
course_instance.execution_source_path = execution.source_path
course = read_course(course_instance.get_course_file_name())
msteams_api = read_msteams_api(MSTEAMS_API_KEY_FILE_NAME)

if get_me_for_check(msteams_api.gen_token) is None:
    token = get_access_token(msteams_api.tenant_id, msteams_api.client_id)
    print(token)
    msteams_api.gen_token = token
    with open(MSTEAMS_API_KEY_FILE_NAME, 'w') as f:
        dict_result = msteams_api.to_json()
        json.dump(dict_result, f, indent=2)

for team in teams:
    print("Team:", get_team(msteams_api.gen_token, team))
print(f"Aantal studenten {len(course.students)}, aantal teams {len(teams)}")
student_count = 1
if len(teams) > 0:
    for student in course.students:
        print("GCH10 -", student_count+1, student.email)
        if len(student.email) > 0:
            team_id = teams[student_count % len(teams)]
            email_parts = student.email.split("@")
            if len(email_parts) > 1:
                # print(student.email)
                channel_id = create_channel(msteams_api.gen_token, team_id, email_parts[0])
                if channel_id:
                    print("GCH12", student.email)
                    add_member_to_team(msteams_api.gen_token, team_id, student.email)
                    add_member_to_channel(msteams_api.gen_token, team_id, channel_id, student.email)
                student_count += 1
        else:
            print("GHC11 -Student heeft geen email", student.name)


    # teams = {"TICT-ICT-V1A-24-TEST": {'id': "b7cf78ae-8c6f-460d-a47a-d4bc2b8b2f18"}}
    #
    # for group in course.student_groups:
    #     if len(group.students) > 30:
    #         print("GC11 - ERROR - Te veel studenten in de groep (", group.name, "). Maximaal 30 studenten, gevonden", len(group.students), "studenten")
    #     else:
    #         print("GC12 - Voor groep (", group.name, ")", len(group.students), "studenten gevonden")
    #         for student_link in group.students:
    #             student = course.find_student(student_link.id)
    #             if student is not None:
    #                 team = teams[group.name].values()
    #                 team_id = team['id']
    #                 channel_id = create_channel(msteams_api.gen_token, team_id, student.name)
    #                 if channel_id:
    #                     print(channel_id, student.email)
    #                     add_member_to_team(msteams_api.gen_token, team_id, student.email)
    #                     add_member_to_channel(msteams_api.gen_token, team_id, channel_id, student.email)
    #                 student_count += 1

    # with open(instances.get_course_file_name(instances.current_instance), 'w') as f:
    #     dict_result = course.to_json(["assignment"])
    #     json.dump(dict_result, f, indent=2)


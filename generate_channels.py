import json
import requests

from lib.config import plot_path
from lib.file import read_start, read_course
from lib.translation_table import translation_table

start = read_start()
course = read_course(start.course_file_name)

CLIENT_SECRET = "eyJ0eXAiOiJKV1QiLCJub25jZSI6ImU0NEtPcG1rVFVJUVJzRlJnbHBNR1B4OWdTS2VuMkllWGRBUjFuU1N5STgiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC85ODkzMjkwOS05YTVhLTRkMTgtYWNlNC03MjM2YjViNWUxMWQvIiwiaWF0IjoxNjk1ODg3NzYxLCJuYmYiOjE2OTU4ODc3NjEsImV4cCI6MTY5NTg5MjAwNiwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhVQUFBQUZ0enhXZlU4WlJJM05XRUZ5eDdJbWNYYTdkMEh1bTV4YnMwYmpZYjB3RnFJMENHT3hNK280T1E5bTYxZ3luZXVNSWNldVNGU2QwWUcrUVd0dTMyTkc3aWsxNzg5MEFIclFjVlFUc3NiRTBvPSIsImFtciI6WyJ3aWEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiRFBXIFRlYW1zIE93bmVyIEF1dG9tYXRpb24gQXBwIiwiYXBwaWQiOiIxODRmMWI0YS1jMGZlLTRhODEtYjY4MC01ZWFiOGM5MGVlYjAiLCJhcHBpZGFjciI6IjAiLCJmYW1pbHlfbmFtZSI6IldpbGtlbnMiLCJnaXZlbl9uYW1lIjoiQmVyZW5kIiwiaWR0eXAiOiJ1c2VyIiwiaW5fY29ycCI6InRydWUiLCJpcGFkZHIiOiIxNDUuODkuMTcwLjMyIiwibmFtZSI6IkJlcmVuZCBXaWxrZW5zIiwib2lkIjoiMjlmZjI4MTgtMzFlMC00MzRjLThjMzAtNTBjYTA0ZGYwYTEyIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTE3NTc0MzYyNjYtMTA3MDM3OTMyNi0xNDUyNzYzMTYxLTY3NDM3IiwicGxhdGYiOiIzIiwicHVpZCI6IjEwMDMzRkZGODYyMjhDRTUiLCJyaCI6IjAuQVFJQUNTbVRtRnFhR0UyczVISTJ0YlhoSFFNQUFBQUFBQUFBd0FBQUFBQUFBQUFDQUpBLiIsInNjcCI6IkNoYW5uZWwuQ3JlYXRlIENoYW5uZWxNZW1iZXIuUmVhZFdyaXRlLkFsbCBHcm91cC5SZWFkV3JpdGUuQWxsIFRhc2tzLlJlYWRXcml0ZSBUYXNrcy5SZWFkV3JpdGUuU2hhcmVkIFRlYW1NZW1iZXIuUmVhZFdyaXRlLkFsbCBVc2VyLlJlYWQgcHJvZmlsZSBvcGVuaWQgZW1haWwiLCJzdWIiOiJrNmVDZThGcTNvYjdJSUZyaVVVeV9vLTRoUV96NDBITVhDMENqZDNMMnZzIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkVVIiwidGlkIjoiOTg5MzI5MDktOWE1YS00ZDE4LWFjZTQtNzIzNmI1YjVlMTFkIiwidW5pcXVlX25hbWUiOiJiZXJlbmQud2lsa2Vuc0BodS5ubCIsInVwbiI6ImJlcmVuZC53aWxrZW5zQGh1Lm5sIiwidXRpIjoiajk2WVpjTjFSa3VucXhVMHFNUTFBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19zdCI6eyJzdWIiOiJXdmFjWjBvQ3RFekJLSkJzdnBINFYzU3RObW9DQzhKaThkSDl5QXFranNJIn0sInhtc190Y2R0IjoxMzQxOTIwNDkwLCJ4bXNfdGRiciI6IkVVIn0.RNTcvrE_XrpM9zHR_OTM37pH337O8oBZzGiEtF0rbux6FrQiLra6gKbBNZTCSSfXsc-aHzG2KWg5GNhc8k2ual0j7C8EoAE1_o2An88Fbek0zJtJAFVE3PO6CzlGGacfFRw__v2xCw-xOD-EAVuvcESnks6h7gKovnBf7qPP0OOdOgoQZPFvNTcSff8HOdk17x-S-JzOMZcpeDovegD3pcwQX3jsNTxUlTzLLqPYrl6M-KB0Ao_n17HgGoU7UQXKUYAFb9LuNQ0p-8pXJe5aL4PmPT3i-1a3D8a-c1RWfEHpyvC6xp9opsRYOmHDCCZR8z7CNN_lm6DX3eOwnFcnjg"


def AddUserToGroup(user, group_id):
    """
        Adds a user to an AAD group
        User = User object from GetUserByEmail()
        group_id = AAD group id
    """
    headers = {"AUTHORIZATION": f"Bearer {CLIENT_SECRET}", "Content-type": "application/json"}
    url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref"
    data = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{user['id']}"
    }
    response = requests.post(url=url, headers=headers, json=data)

    if response.status_code == 204:
        print(f"User {user['displayName']} added to group: {response.status_code}")
    elif response.status_code == 400:
        print.error(f"ERROR: User {user['displayName']} already exist in the group: {response.status_code}")
    elif response.status_code == 404:
        print.error(f"ERROR: User {user['displayName']} or group not found: {response.status_code}")

CLIENT_ID = "184f1b4a-c0fe-4a81-b680-5eab8c90eeb0"
TENANT_ID = "98932909-9a5a-4d18-ace4-7236b5b5e11d"
RedirectURI = "https://localhost"
tenantname = "hogeschoolutrecht.onmicrosoft.com"



# url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
# headers = {
#     "Authorization": "Bearer "+CLIENT_SECRET,
#     "Content-Type": "application/x-www-form-urlencoded"
# }
# data = {
#     "grant_type": "client_credentials",
#     "client_id": CLIENT_ID,
#     "client_secret": CLIENT_SECRET,
#     "scope": "https://graph.microsoft.com/.default"
# }
#
g_team_ids = ["b7cf78ae-8c6f-460d-a47a-d4bc2b8b2f18", "2d570ef0-7a51-489e-a2e3-681440e67d08", "82e424d3-5baa-4ba2-b2f8-85b3659a150e", "a282ec15-7540-4c3b-bb3c-26b2f38377c7"]
# url = f"https://graph.microsoft.com/v1.0/teams/{TEAM_ID}/"
# # url = "https://graph.microsoft.com/v1.0/me/joinedTeams"
# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     result = response.json()
#     print(result['displayName'])
#     with open('dump.json', 'w') as f:
#         json.dump(result, f, indent=2)
# else:
#     print(f"Error getting token: {response.json()}")

def get_channels(a_team_id):
    url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels"
    print(url)
    headers = {
        "Authorization": "Bearer " + CLIENT_SECRET,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(url, headers=headers)
    l_channels = {}
    if response.status_code == 200:
        result = response.json()
        values = result['value']
        for value in values:
            print(value['displayName'], value['id'])
            l_channels[value['displayName']] = value['id']
        # with open('teams-api/dump.json', 'w') as f:
        #     json.dump(result, f, indent=2)
    else:
        print(f"Error getting token: {response.json()}")
    return l_channels


def create_channel(a_team_id, a_diplay_name):
    l_headers = {
        "Authorization": "Bearer "+CLIENT_SECRET,
        "Content-Type": "application/json"
    }
    l_data = {
        'displayName': a_diplay_name,
        'description': 'In dit kanaal wordt je persoonlijke dashboard geplaatst.',
        "membershipType": "private"
    }

    l_json_object = json.dumps(l_data)
    # print(l_json_object)
    l_url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels"
    print(l_url)
    response = requests.post(l_url, headers=l_headers, data=l_json_object)
    if response.status_code == 201:
        l_result = response.json()
        with open('teams-api/dump.json', 'w') as f:
            json.dump(l_result, f, indent=2)
    else:
        print(f"Response: {response.json()}")

print(len(course.students))
for l_team_id in g_team_ids:
    l_channels = get_channels(l_team_id)
    for l_channel in l_channels:
        course.remove_student_by_name(l_channel)
print(len(course.students))


l_team_id = g_team_ids[3]
for l_student in course.students:
    print('Student:', l_student.name)
    create_channel(l_team_id, l_student.name)

for l_team_id in g_team_ids:
    l_channels = get_channels(l_team_id)
    for l_channel in l_channels:
        course.remove_student_by_name(l_channel)
print(len(course.students))


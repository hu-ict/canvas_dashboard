import subprocess
import io
import json
import requests

from lib.file import read_msteams_api, read_course, read_start
from lib.teams_api_lib import get_me_for_check, get_access_token, get_sites

"""
Module om een MStoken op te halen bij Microsoft
De module voert een PowerShell Module uit, en vangt
de resulterende JSON-response op, waarna een JWT-token 
uit de response wordt gehaald.

Benodigd zijn de PowerShell module MSAL.PS 4.37.0.0 en de juiste policy:
    Install-Module -Name MSAL.PS -RequiredVersion 4.37.0.0
    Set-ExecutionPolicy RemoteSigned

    Achterhalen welke versie/policy je nu hebt:
        Get-InstalledModule -AllVersions MSAL.PS
        Get-ExecutionPolicy

    Uninstall version:
        Uninstall-Module -AllVersions MSAL.PS

    Import specific version:
        Import-Module -RequiredVersion 4.37.0.0 MSAL.PS

Communicatie met de Graph API wordt daardoor mogelijk
via Python. Voor toekomstig gebruik; in deze repository
is deze code nog niet in gebruik, 

Bart van Eijkelenburg (bart.vaneijkelenburg@hu.nl)
"""

def create_channel_in_team(a_token, a_team_id, a_display_name):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "application/json"
    }
    l_data = {
        'displayName': a_display_name,
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
        print(l_result['id'])
        return(l_result['id'])
    else:
        print(f"Response: {response.json()}")
        return None

def add_team_member(token, team_id, member_id):
    print(f"Sending Request to add a member in a team {team_id}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-type": "application/json; charset=ISO-8859-1"
    }

    body_json_member = {
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["member"],
        "user@odata.bind" : f"https://graph.microsoft.com/v1.0/users/{member_id}"
    }

    url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/members"
    response = requests.post(url, json=body_json_member, headers=headers)
    print(json.dumps(response.json(), indent=2))


def add_channel_member(a_token, team_id, channel_id, member_id):
    print(f"Sending Request to add a member in a channel Team[{team_id}], Channel[{channel_id}]")
    l_headers = {
        "Authorization": f"Bearer {a_token}",
        "Content-type": "application/json; charset=ISO-8859-1"
    }
    l_body_json = {
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["member"],
        "user@odata.bind" : f"https://graph.microsoft.com/v1.0/users/{member_id}"
    }
    l_url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/members"
    response = requests.post(l_url, headers=l_headers, data=l_body_json)
    if response.status_code == 201:
        l_result = json.dumps(response.json(), indent=2)
        print(l_result)
    else:
        print(f"Response: {response.json()}")


if __name__ == "__main__":
    course_config_start = read_start()
    course = read_course(course_config_start.course_file_name)
    msteams_api = read_msteams_api("msteams_api.json")
    team_ids = ["b7cf78ae-8c6f-460d-a47a-d4bc2b8b2f18", "2d570ef0-7a51-489e-a2e3-681440e67d08",
                  "82e424d3-5baa-4ba2-b2f8-85b3659a150e", "a282ec15-7540-4c3b-bb3c-26b2f38377c7"]
    team = "a282ec15-7540-4c3b-bb3c-26b2f38377c7"
    channel = "19:38c8f65e679a40d998ee1086fce55055@thread.tacv2"
    if get_me_for_check(msteams_api.token) == None:
        token = get_access_token()
        print(token)
        msteams_api.token = token
        with open("msteams_api.json", 'w') as f:
            dict_result = msteams_api.to_json()
            json.dump(dict_result, f, indent=2)
    # team_members = get_team_members(msteams_api.token, team)
    course = get_sites(course, msteams_api.token)
    if course != None:
        with open(course_config_start.course_file_name, 'w') as f:
            dict_result = course.to_json(["assignment"])
            json.dump(dict_result, f, indent=2)

    # add_team_member(token, team, "dion.dresschers@hu.nl")
    # create_channel_in_team(a_token=msteams_api.token, a_team_id=team, a_diplay_name="Berend J. Wilkens")
    # add_channel_member(token, team, channel, "dion.dresschers@hu.nl")



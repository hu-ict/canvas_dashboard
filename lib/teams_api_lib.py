import json
import requests
from lib.translation_table import translation_table
import subprocess
import io

teams = ["1221c52c-8dde-4f0a-8dd2-fafe98df6c2d",
         "6cc9038c-76d1-4c7d-a40a-87b04d2e6d2f",
         "c9f90014-7843-4e2c-92c2-2727b5d20ede",
         "8a2cfa62-5ec8-4266-b2bc-4f1fed73cf6c",
         "02a1e0ea-46c9-460a-956a-5f9ad7302ee6"]
# https://teams.microsoft.com/l/team/19%3AcxEwbQY-TpX23Y4slSrFCWgIutGGF2JDk829QxLhmFY1%40thread.tacv2/conversations?groupId=8d309e88-cdae-4720-aed8-47384bc36820&tenantId=98932909-9a5a-4d18-ace4-7236b5b5e11d
# https://teams.microsoft.com/l/team/19%3A3l-_a4EUOq-9AwvkU6dAVddcELw_bL3xU0xW2-hKWmg1%40thread.tacv2/conversations?groupId=59a9f9c3-4a23-4f74-ad75-a269f0e70891&tenantId=98932909-9a5a-4d18-ace4-7236b5b5e11d
# https://teams.microsoft.com/l/team/19%3AJ0cuUcTJg79b1IGafrNhQxKV8xJSgIgP9BoDhBUEZOM1%40thread.tacv2/conversations?groupId=f66f15ab-36cf-4af7-8e36-9f380e8f8a5c&tenantId=98932909-9a5a-4d18-ace4-7236b5b5e11d
# https://teams.microsoft.com/l/team/19%3AOUGszdnbXVRK76ZqNgLxZkTRa80goO2f3ozej08peGA1%40thread.tacv2/conversations?groupId=68ab52d4-8c10-4316-9a88-229854794074&tenantId=98932909-9a5a-4d18-ace4-7236b5b5e11d

def get_access_token(a_tenant_id, a_client_id):
    print("get_access_token", a_tenant_id, a_client_id)
    redirect_uri = "https://localhost"

    captured_output = io.StringIO()
    command = f"Get-MsalToken -DeviceCode -ClientId {a_client_id} -TenantId {a_tenant_id} -RedirectUri {redirect_uri}|ConvertTo-JSON"
    process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True)
    while process.poll() is None:
        char = process.stdout.read(1)

        if char == "\n":
            break

        print(char, end="", flush=True)

    chars = process.stdout.readlines()
    captured_output.writelines(chars)

    resulting_object = captured_output.getvalue()
    # print(resulting_object)
    obj = json.loads(resulting_object)

    print("Accesstoken: ", obj["AccessToken"])
    return obj["AccessToken"]


def get_me_for_check(a_token):
    print(f"Sending Request to ask for me")
    headers = {
        "Authorization": f"Bearer {a_token}",
        "Content-type": "application/json; charset=ISO-8859-1"
    }
    url = f"https://graph.microsoft.com/v1.0/me"
    print(url)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        l_result = response.json()
        print(l_result['displayName'])
        return(l_result['displayName'])
    else:
        print(f"Response {url}: {response.json()}")
        return None


def add_user_to_group(a_token, a_group, a_user):
    """
        Adds a user to an AAD group
        User = User object from GetUserByEmail()
        group_id = AAD group id
    """
    headers = {"AUTHORIZATION": f"Bearer {a_token}", "Content-type": "application/json"}
    url = f"https://graph.microsoft.com/v1.0/groups/{a_group}/members/$ref"
    data = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/directoryObjects/{a_user['id']}"
    }
    response = requests.post(url=url, headers=headers, json=data)

    if response.status_code == 204:
        print(f"User {a_user['displayName']} added to group: {response.status_code}")
    elif response.status_code == 400:
        print.error(f"ERROR: User {a_user['displayName']} already exist in the group: {response.status_code}")
    elif response.status_code == 404:
        print.error(f"ERROR: User {a_user['displayName']} or group not found: {response.status_code}")


def get_member_id(a_token, a_email):
    url = f"https://graph.microsoft.com/v1.0/users/{a_email}"
    headers = {
        "Authorization": "Bearer " + a_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        member_id = result['id']
        return member_id
    else:
        print(f"Error getting member_id: {response}")
        return None


def get_team_members(a_token, team_id):
    print(f"Sending Request to get team members Team[{team_id}]")
    l_members = {}
    headers = {
        "Authorization": f"Bearer {a_token}",
        "Content-type": "application/json; charset=ISO-8859-1"
    }
    url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/members"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        values = result['value']
        for value in values:
            print(value['displayName'], value['id'])
            l_members[value['displayName']] = value['id']
    else:
        print(f"Response error: {response.json()}")


def get_team_channels(a_token, a_team_id):
    url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels"
    headers = {
        "Authorization": "Bearer " + a_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    l_channels = {}
    if response.status_code == 200:
        result = response.json()
        values = result['value']
        for value in values:
            # print("get_team_channels", value['displayName'], value['id'])
            l_channels[value['displayName']] = value['id']
        return l_channels
    else:
        print(f"Response error: {response.json()}")
        return None


def get_sites(a_token, a_query):
    url = f"https://graph.microsoft.com/v1.0/sites?search={a_query}"
    headers = {
        "Authorization": "Bearer " + a_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        values = result['value']
        print("TA41 - Aantal sites:", len(values))
        names = {}
        for value in values:
            # print("TA44 -", value)
            # "INNO - Sep23 - Studenten - Kyrill Westdorp"
            l_display_name = value['displayName']
            print("TA45 - DisplayName:", l_display_name)
            l_display_name_split = l_display_name.split(' - ')
            if len(l_display_name_split) > 3:
                l_student_name = l_display_name_split[3]
                names[l_student_name] = value['id']
                print("TA46 - Student:", l_student_name)
            else:
                print("TA47 - DisplayName doesn't contain a student name")
        return names
    else:
        print(f"TA48 - Error getting token: {response.json()}")
        return None


def get_site_id(a_token, a_student):
    print(a_student)
    l_site_name = a_student.translate(translation_table)
    # l_site_name = remove_spaces(l_site_name)

    url = f"https://graph.microsoft.com/v1.0/sites?search={l_site_name}"
    print(url)
    headers = {
        "Authorization": "Bearer " + a_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        values = result['value']
        print("Values", values)
        for value in values:
            print(value['id'])
            return value['id']
    else:
        print(f"Error getting token: {response.json()}")
    return None


def upload_file_to_teams(a_token, a_channel, a_source_filename, a_remote_filename, a_name):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "application/html"
    }

    asci_source_file_name = a_source_filename.translate(translation_table)
    # asci_source_file_name = asci_source_file_name.replace(" ", "%20")
    asci_remote_file_name = a_remote_filename.translate(translation_table)
    asci_remote_file_name = asci_remote_file_name.replace(" ", "%20")
    a_channel = "19%3Af51e6d4cce424fc4a906b4cc78748bd3%40thread.tacv2"
    a_name = a_name.replace(" ", " ")
    # PUT /groups/{group-id}/drive/items/{parent-id}:/{filename}:/content
    # PUT /sites/{site-id}/drives/{drive-id}/{parent-id}:/{filename}:/content
    print("TA22 - Remote filename", asci_remote_file_name)
    with open(asci_source_file_name, mode='r', encoding="utf-8") as file_plotly:
        data = file_plotly.read()
    l_url = f"https://graph.microsoft.com/v1.0/sites/{a_channel}/drive/items/root:/{asci_remote_file_name}:/content"
    print("TA23 -", l_url)
    response = requests.put(l_url, headers=l_headers, data=data)
    if response.status_code != 200:
        print(f"Error {response.status_code} response: {response.json()}")

def upload_file_to_onedrive(a_token, a_name, a_drive_id, a_file_path, a_file_name):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "image/jpeg"
    }
    # print(l_headers)
    file_name_html = a_file_path + a_file_name
    asci_file_name = file_name_html.translate(translation_table)
    l_remote_file_name = a_file_name.translate(translation_table)
    with open(asci_file_name, mode='rb') as file_plotly:
        data = file_plotly.read()

    # drive_id = "b!JlWXSwZ06kqtE18zUw4nyLLiywuLAR9AiyKsmQ1pD5H1RQraPukJRoocfQ2Oj64W"
    # l_url = f"https://graph.microsoft.com/v1.0/sites/{a_channel}/drive/items/root:/{a_name}/{l_remote_file_name}%20progress.jpeg:/content"
    url = f"https://graph.microsoft.com/v1.0/drives/{a_drive_id}/items/root:/{a_name.replace(' ', '%20')}/{l_remote_file_name.replace(' ', '%20')}:/content"
    print(url)
    response = requests.put(url, headers=l_headers, data=data)
    if response.status_code not in [200, 201]:
        print(f"Error {response.status_code} response: {response.json()}")



def create_channel(a_token, a_team_id, a_diplay_name):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "application/json"
    }
    l_data = {
        'displayName': a_diplay_name,
        'description': 'In dit kanaal wordt je persoonlijke INNO-dashboard geplaatst.',
        "membershipType": "private"
    }
    l_json_object = json.dumps(l_data)
    print(l_json_object)
    l_url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels"
    print(l_url)
    response = requests.post(l_url, headers=l_headers, data=l_json_object)
    if response.status_code == 201:
        l_result = response.json()
        with open('teams-api/dump.json', 'w') as f:
            json.dump(l_result, f, indent=2)
        return l_result["id"]
    print(f"TA04 - Response: {response.json()}")
    return None



def add_member_to_team(a_token, a_team_id, a_member_login):
    headers = {
        "Authorization": f"Bearer {a_token}",
        "Content-type": "application/json; charset=ISO-8859-1"
    }
    body_json_member = {
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["member"],
        "user@odata.bind" : f"https://graph.microsoft.com/v1.0/users/{a_member_login}"
    }
    url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/members"
    response = requests.post(url, json=body_json_member, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"TA05 - Error response: {response.json()}")
        return None


def add_member_to_channel(a_token, a_team_id, a_channel_id, a_member_login):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "application/json"
    }
    l_data = {
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["owner"],
        "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{a_member_login}')"
    }
    l_url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels/{a_channel_id}/members"
    l_json_object = json.dumps(l_data)
    response = requests.post(l_url, headers=l_headers, data=l_json_object)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"TA14 - Error response: {response.json()}")
        return None

def get_channels(a_token, a_team_id):
    url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels"
    print("TA21 -", url)
    headers = {
        "Authorization": "Bearer " + a_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        values = result['value']
        channels = []
        for value in values:
            # print("TA27 -", value)
            channel = {"display_name": value["displayName"], "id": value["id"]}
            # print("TA22 -", channel)
            channels.append(channel)
        return channels
    else:
        print(f"TA24 - Error getting token: {response.json()}")
    return []


def get_team(a_token, a_team_id):
    url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}"
    # print("TA36 -", url)
    headers = {
        "Authorization": "Bearer " + a_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return {"displayName": result['displayName'], "members": result['summary']['membersCount']}
    else:
        return f"TA38 - Error getting token: {response.json()}"


def get_drive(token, team_id, channel_id):
    url = f"https://graph.microsoft.com/v1.0/teams/{team_id}/channels/{channel_id}/filesFolder"
    # print("TA36 -", url)
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return {"display_name": result['name'], "drive_id": result['parentReference']['driveId']}
    else:
        print(f"TA38 - Error getting token: {response.json()}")
    return {"display_name": "", "drive_id": ""}


def send_mail(token, recipient, body):
    l_headers = {
        "Authorization": "Bearer "+token,
        "Content-Type": "application/json"
    }
    l_data = {"message": {
                "subject": "Meet for lunch?",
                "body": {
                    "contentType": "Text",
                    "content": "The new cafeteria is open."
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": "anita.grit@hu.nl"
                        }
                    }
                ]
            }
        }
    l_json_object = json.dumps(l_data)
    print(l_json_object)
    l_url = f"https://graph.microsoft.com/v1.0/me/sendMail"
    print(l_url)
    response = requests.post(l_url, headers=l_headers, data=l_json_object)
    if response.status_code == 201:
        l_result = response.json()
        with open('teams-api/dump.json', 'w') as f:
            json.dump(l_result, f, indent=2)
        return l_result
    print(f"TA04 - Response: {response.json()}")
    return None


import json
import requests
from lib.translation_table import translation_table
import subprocess
import io

teams = ["943b34c2-39cc-44d2-8251-88b75a835cfc", "d1f12dcf-875b-4d0c-bba6-262b3b57daea", "1b8c2e9b-8c84-4e1d-af12-1ea4d4aff274", "961f8415-0d43-4f85-94df-4c1e4ec48757"]

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
        print("Aantal sites:",len(values))
        names = {}
        for value in values:
            # "INNO - Sep23 - Studenten - Kyrill Westdorp"
            l_display_name = value['displayName']
            # print("DisplayName:", l_display_name)
            l_display_name_split = l_display_name.split(' - ')
            if len(l_display_name_split) > 3:
                l_student_name = l_display_name_split[3]
                names[l_student_name] =  value['id']
                # print("Student:", l_student_name)
            else:
                print("DisplayName doesn't contain a student name")
        return names
    else:
        print(f"Error getting token: {response.json()}")
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


def upload_file_html(a_token, a_plot_path, a_name, a_channel):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "application/html"
    }
    file_name_html = a_plot_path + a_name + ".html"
    asci_file_name = file_name_html.translate(translation_table)
    l_remote_file_name = a_name.translate(translation_table)
    with open(asci_file_name, mode='r', encoding="utf-8") as file_plotly:
        data = file_plotly.read()
    l_url = f"https://graph.microsoft.com/v1.0/sites/{a_channel}/drive/items/root:/{a_name}/{l_remote_file_name}.html:/content"
    response = requests.put(l_url, headers=l_headers, data=data)
    if response.status_code != 200:
        print(f"Error {response.status_code} response: {response.json()}")

def upload_file_jpeg(a_token, a_plot_path, a_name, a_channel):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "image/jpeg"
    }
    file_name_html = a_plot_path + a_name + ".jpeg"
    asci_file_name = file_name_html.translate(translation_table)
    l_remote_file_name = a_name.translate(translation_table)
    with open(asci_file_name, mode='rb') as file_plotly:
        data = file_plotly.read()
    l_url = f"https://graph.microsoft.com/v1.0/sites/{a_channel}/drive/items/root:/{a_name}/{l_remote_file_name}.jpeg:/content"
    response = requests.put(l_url, headers=l_headers, data=data)
    if response.status_code != 200:
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
    print(f"Response: {response.json()}")
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
        print(f"Error response: {response.json()}")
        return None


def add_member_to_channel(a_token, a_team_id, a_channel_id, a_member_login):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "application/json"
    }
    l_data = {
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["member"],
        "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{a_member_login}')"
    }
    l_url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels/{a_channel_id}/members"
    l_json_object = json.dumps(l_data)
    response = requests.post(l_url, headers=l_headers, data=l_json_object)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error response: {response.json()}")
        return None

def get_channels(a_token, a_team_id):
    url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels"
    print(url)
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
            channels.append(value['displayName'])
        return channels
    else:
        print(f"Error getting token: {response.json()}")
    return None

def get_team(a_token, a_team_id):
    url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}"
    print(url)
    headers = {
        "Authorization": "Bearer " + a_token,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return {"displayName": result['displayName'], "members": result['summary']['membersCount']}
    else:
        print(f"Error getting token: {response.json()}")
    return None

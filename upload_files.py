import json
import requests

from lib.config import plot_path
from lib.file import read_start, read_course, read_msteams_api
from lib.translation_table import translation_table

# start = read_start()
# course = read_course(start.course_file_name)
#
# CLIENT_SECRET = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Iko1MWREbkl1Q2w3VWVNN0NBV1ZsMTh0RDZKWXlEeUM5cm1mV2pnZVFrNkkiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiIwMDAwMDAwMy0wMDAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC85ODkzMjkwOS05YTVhLTRkMTgtYWNlNC03MjM2YjViNWUxMWQvIiwiaWF0IjoxNjk1NzI1ODk1LCJuYmYiOjE2OTU3MjU4OTUsImV4cCI6MTY5NTgxMjU5NSwiYWNjdCI6MCwiYWNyIjoiMSIsImFpbyI6IkFWUUFxLzhVQUFBQXdVZnNTOVdOS0xjZWRPVGxzYW1mZmpkcWJQc0hVUHUyQ1ZZNkt0NXhWUFZVcDVYM1NRVllQMEZEMTdIV2NBNVFpV2pqVlEvOVRhdmlvemtOZDlGbHVUNGE3emh1Qkd0K0srYlJQeWs0bFJRPSIsImFtciI6WyJwd2QiLCJyc2EiLCJtZmEiXSwiYXBwX2Rpc3BsYXluYW1lIjoiR3JhcGggRXhwbG9yZXIiLCJhcHBpZCI6ImRlOGJjOGI1LWQ5ZjktNDhiMS1hOGFkLWI3NDhkYTcyNTA2NCIsImFwcGlkYWNyIjoiMCIsImRldmljZWlkIjoiYTBjODI2YWYtMDNhMC00ZTY2LTlmNzEtMGQ3ZGVkYmU0MTU0IiwiZmFtaWx5X25hbWUiOiJXaWxrZW5zIiwiZ2l2ZW5fbmFtZSI6IkJlcmVuZCIsImlkdHlwIjoidXNlciIsImlwYWRkciI6IjIwMDE6MWMwMjoyYjA1OmNmMDA6ZGRlOTpmNTI3OmRmNDY6NWE5YyIsIm5hbWUiOiJCZXJlbmQgV2lsa2VucyIsIm9pZCI6IjI5ZmYyODE4LTMxZTAtNDM0Yy04YzMwLTUwY2EwNGRmMGExMiIsIm9ucHJlbV9zaWQiOiJTLTEtNS0yMS0xNzU3NDM2MjY2LTEwNzAzNzkzMjYtMTQ1Mjc2MzE2MS02NzQzNyIsInBsYXRmIjoiMyIsInB1aWQiOiIxMDAzM0ZGRjg2MjI4Q0U1IiwicHdkX2V4cCI6IjQxNDgxOSIsInB3ZF91cmwiOiJodHRwczovL3N0cy5odS5ubC9hZGZzL3BvcnRhbC91cGRhdGVwYXNzd29yZC8iLCJyaCI6IjAuQVFJQUNTbVRtRnFhR0UyczVISTJ0YlhoSFFNQUFBQUFBQUFBd0FBQUFBQUFBQUFDQUpBLiIsInNjcCI6IkF1ZGl0TG9nLlJlYWQuQWxsIENhbGVuZGFycy5SZWFkV3JpdGUgQ29udGFjdHMuUmVhZFdyaXRlIERldmljZU1hbmFnZW1lbnRBcHBzLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRBcHBzLlJlYWRXcml0ZS5BbGwgRGV2aWNlTWFuYWdlbWVudENvbmZpZ3VyYXRpb24uUmVhZC5BbGwgRGV2aWNlTWFuYWdlbWVudENvbmZpZ3VyYXRpb24uUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50TWFuYWdlZERldmljZXMuUHJpdmlsZWdlZE9wZXJhdGlvbnMuQWxsIERldmljZU1hbmFnZW1lbnRNYW5hZ2VkRGV2aWNlcy5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50TWFuYWdlZERldmljZXMuUmVhZFdyaXRlLkFsbCBEZXZpY2VNYW5hZ2VtZW50UkJBQy5SZWFkLkFsbCBEZXZpY2VNYW5hZ2VtZW50UkJBQy5SZWFkV3JpdGUuQWxsIERldmljZU1hbmFnZW1lbnRTZXJ2aWNlQ29uZmlnLlJlYWQuQWxsIERldmljZU1hbmFnZW1lbnRTZXJ2aWNlQ29uZmlnLlJlYWRXcml0ZS5BbGwgRGlyZWN0b3J5LkFjY2Vzc0FzVXNlci5BbGwgRGlyZWN0b3J5LlJlYWQuQWxsIERpcmVjdG9yeS5SZWFkV3JpdGUuQWxsIEZpbGVzLlJlYWRXcml0ZS5BbGwgR3JvdXAuUmVhZC5BbGwgR3JvdXAuUmVhZFdyaXRlLkFsbCBJZGVudGl0eVJpc2tFdmVudC5SZWFkLkFsbCBNYWlsLlJlYWRXcml0ZSBNYWlsYm94U2V0dGluZ3MuUmVhZFdyaXRlIE5vdGVzLlJlYWRXcml0ZS5BbGwgb3BlbmlkIFBlb3BsZS5SZWFkIHByb2ZpbGUgUmVwb3J0cy5SZWFkLkFsbCBTaXRlcy5SZWFkV3JpdGUuQWxsIFRhc2tzLlJlYWRXcml0ZSBUZWFtc0FwcEluc3RhbGxhdGlvbi5SZWFkRm9yVGVhbSBUZWFtc0FwcEluc3RhbGxhdGlvbi5SZWFkV3JpdGVGb3JUZWFtIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgVXNlci5SZWFkV3JpdGUgVXNlci5SZWFkV3JpdGUuQWxsIGVtYWlsIiwic2lnbmluX3N0YXRlIjpbImR2Y19tbmdkIiwiZHZjX2RtamQiLCJrbXNpIl0sInN1YiI6Ims2ZUNlOEZxM29iN0lJRnJpVVV5X28tNGhRX3o0MEhNWEMwQ2pkM0wydnMiLCJ0ZW5hbnRfcmVnaW9uX3Njb3BlIjoiRVUiLCJ0aWQiOiI5ODkzMjkwOS05YTVhLTRkMTgtYWNlNC03MjM2YjViNWUxMWQiLCJ1bmlxdWVfbmFtZSI6ImJlcmVuZC53aWxrZW5zQGh1Lm5sIiwidXBuIjoiYmVyZW5kLndpbGtlbnNAaHUubmwiLCJ1dGkiOiI4V19faEJNbFBreVhKQnpEYUFFSUFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2NjIjpbIkNQMSJdLCJ4bXNfc3NtIjoiMSIsInhtc19zdCI6eyJzdWIiOiJ1LUsxaXlkQThjX3NNZERoeXRJOFI3SjIwcjBWaU1GNk9zYWhFLUFld2pVIn0sInhtc190Y2R0IjoxMzQxOTIwNDkwLCJ4bXNfdGRiciI6IkVVIn0.Vbv25626TBn74I8HUz37m_AnexkypWlOmfx-6UkVNMbF9wFUXnoNmp3KGmoK7X-e5Dwy_ISrJRajUJFGchrGvYB1teP6X70BsKigu5_9Rug_LAYzoRr4YXcYcIiVKNE2XO_X5TmpfSmQ7bcLe8CvScmXGyWFBw_ronvGMxpvfwjMhzHGFTOed5E2YVbZoIMVlgOY3pnq4JOwQCof8Y0O6lJHLiFCHARD71SaUevKOkvpKpLDnAlhfeWobUIKN8aR0vkO8OfsAOoXk-qrC-B8Hy32Vo6cGKr36FQ1yagJEvDAVyr_ODeq7Da66TkTwO5XmxlimBoqMG9ktYyDEu4TqQ"
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

def get_channels(a_token, a_team_id):
    url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels"
    print(url)
    headers = {
        "Authorization": "Bearer " + a_token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(url, headers=headers)
    l_channels = {}
    if response.status_code == 200:
        result = response.json()
        values = result['value']
        print(values)
        for value in values:
            print(value['displayName'], value['id'])
            l_channels[value['displayName']] = value['id']
        with open('teams-api/dump.json', 'w') as f:
            json.dump(result, f, indent=2)
    else:
        print(f"Error getting token: {response.json()}")
    return l_channels


def get_sites(a_token, a_students):
    l_sites = {}
    for l_student in a_students:
        # print(l_student)
        l_site_name = l_student.translate(translation_table)
        # l_site_name = remove_spaces(l_site_name)

        url = f"https://graph.microsoft.com/v1.0/sites?search={l_site_name}"
        # print(url)
        headers = {
            "Authorization": "Bearer " + a_token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()
            values = result['value']
            for value in values:
                l_sites[l_student] = value['id']
        else:
            print(f"Error getting token: {response.json()}")
    return l_sites


def get_site_id(a_token, a_student):

    print(a_student)
    l_site_name = a_student.translate(translation_table)
    # l_site_name = remove_spaces(l_site_name)

    url = f"https://graph.microsoft.com/v1.0/sites?search={l_site_name}"
    print(url)
    headers = {
        "Authorization": "Bearer " + a_token,
        "Content-Type": "application/x-www-form-urlencoded"
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

def add_member_to_channel(a_token, a_team_id, a_channel_id, a_member_id):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "application/json"
    }

    l_data = {
        "@odata.type": "#microsoft.graph.aadUserConversationMember",
        "roles": ["member"],
        "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{a_member_id}')"
    }

    l_url = f"https://graph.microsoft.com/v1.0/teams/{a_team_id}/channels/{a_channel_id}/members"
    l_json_object = json.dumps(l_data)
    response = requests.post(l_url, headers=l_headers, data=l_json_object)
    if response.status_code == 201:
        l_result = response.json()
        with open('teams-api/dump.json', 'w') as f:
            json.dump(l_result, f, indent=2)
    print(f"Response: {response.json()}")

def upload_file(a_token, a_plot_path, a_name, a_channel):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "application/html"
    }
    file_name = a_plot_path + a_name + ".html"
    asci_file_name = file_name.translate(translation_table)
    l_remote_file_name = a_name.translate(translation_table)
    with open(asci_file_name, mode='r', encoding="utf-8") as file_plotly:
        data = file_plotly.read()
    l_url = f"https://graph.microsoft.com/v1.0/sites/{a_channel}/drive/items/root:/{a_name}/{l_remote_file_name}.html:/content"
    response = requests.put(l_url, headers=l_headers, data=data)
    if response.status_code == 200:
        l_result = response.json()
        with open('teams-api/dump.json', 'w') as f:
            json.dump(l_result, f, indent=2)
    # print(f"Response: {response.json()}")

def create_channel(a_token, a_team_id, a_diplay_name):
    l_headers = {
        "Authorization": "Bearer "+a_token,
        "Content-Type": "application/json"
    }
    l_data = {
        'displayName': a_diplay_name,
        'description': 'In dit kanaal wordt je persoonlijke dashboard geplaatst.',
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
    print(f"Response: {response.json()}")


course_config_start = read_start()
course = read_course(course_config_start.course_file_name)
msteams_api = read_msteams_api("msteams_api.json")

# print("Sites", g_sites)
for l_student in course.students:
    print('Student:', l_student.name)
    upload_file(msteams_api.token, plot_path, l_student.name, l_student.site)



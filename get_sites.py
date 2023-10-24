import json

from lib.file import read_start, read_course, read_msteams_api
from lib.teams_api_lib import get_sites, get_me_for_check, get_access_token

start = read_start()
course = read_course(start.course_file_name)
msteams_api = read_msteams_api("msteams_api.json")

if get_me_for_check(msteams_api.gen_token) is None:
    print("Obtain new token")
    token = get_access_token(msteams_api.tenant_id, msteams_api.client_id)
    print(token)
    msteams_api.gen_token = token
    with open("msteams_api.json", 'w') as f:
        dict_result = msteams_api.to_json()
        json.dump(dict_result, f, indent=2)

get_sites(msteams_api.my_token, course, "INNO")

with open(start.course_file_name, 'w') as f:
    dict_result = course.to_json(["assignment"])
    json.dump(dict_result, f, indent=2)

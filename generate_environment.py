import json
import os

from scripts.lib.file_const import ENVIRONMENT_FILE_NAME, SECRET_API_KEY_FILE_NAME, ENVIRONMENT_PATH, COURSES_PATH
from scripts.model.environment.Environment import Environment
from scripts.model.environment.Execution import Execution
from scripts.model.environment.SecretApiKey import SecretApiKey

environment_name = input("Give a name for your environment: ")
canvas_api_key = input("Give your personal canvas_api_key: ")
environment = Environment(environment_name, {"course_name": "", "course_instance_name": ""})
environment.executions.append(Execution("env_1", "", ""))
environment.executions.append(Execution("env_2", "", ""))
environment.executions.append(Execution("env_3", "", ""))
secret_api_key = SecretApiKey(environment_name, canvas_api_key)
print("Creating new environment", environment_name)
os.makedirs(ENVIRONMENT_PATH, exist_ok=True)
os.makedirs(COURSES_PATH, exist_ok=True)
with open(ENVIRONMENT_FILE_NAME, 'w') as f:
    dict_result = environment.to_json()
    json.dump(dict_result, f, indent=2)
with open(SECRET_API_KEY_FILE_NAME, 'w') as f:
    dict_result = secret_api_key.to_json()
    json.dump(dict_result, f, indent=2)
print("Environment is created", environment_name)


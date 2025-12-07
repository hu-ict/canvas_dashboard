import json

from model.environment.Environment import Environment, ENVIRONMENT_FILE_NAME
from model.environment.Execution import Execution
from scripts.model.environment.SecretApiKey import SecretApiKey, SECRET_API_KEY_FILE_NAME
from model.environment.Workflow import Workflow, WORKFLOW_FILE_NAME

environment_name = input("Give a name for your environment: ")
canvas_api_key = input("Give your personal canvas_api_key: ")
environment = Environment(environment_name, {"course_name": "", "course_instance_name": ""})
environment.executions.append(Execution("env_1", "", ""))
environment.executions.append(Execution("env_2", "", ""))
environment.executions.append(Execution("env_3", "", ""))
secret_api_key = SecretApiKey(environment_name, canvas_api_key)
workflow = Workflow(environment_name)
workflow.new_instance()
print("Creating new environment", environment_name)
with open(ENVIRONMENT_FILE_NAME, 'w') as f:
    dict_result = environment.to_json()
    json.dump(dict_result, f, indent=2)
with open(SECRET_API_KEY_FILE_NAME, 'w') as f:
    dict_result = secret_api_key.to_json()
    json.dump(dict_result, f, indent=2)
with open(WORKFLOW_FILE_NAME, 'w') as f:
    dict_result = workflow.to_json()
    json.dump(dict_result, f, indent=2)
print("Environment is created", environment_name)


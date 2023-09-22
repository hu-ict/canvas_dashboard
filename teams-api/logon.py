import json

import msal
from msal import ConfidentialClientApplication, PublicClientApplication

CLIENT_ID = "184f1b4a-c0fe-4a81-b680-5eab8c90eeb0"
TENANT_ID = "98932909-9a5a-4d18-ace4-7236b5b5e11d"
RedirectURI = "https://localhost"
TENANT_NAME = "hogeschoolutrecht.onmicrosoft.com"
TENANT_NAME_SHORT = "hogeschoolutrecht"
scopes = ["https://"+TENANT_NAME+"/.default"]

auth = f"https://login.microsoftonline.com/{TENANT_ID}"
tenant = f"https://{TENANT_NAME}.b2clogin.com/{TENANT_NAME}.onmicrosoft.com/B2C_1_signup_signin_policy",

# app = PublicClientApplication(
#     client_id=CLIENT_ID,
#     client_credential=None,
#     authority=tenant
# )
# s = "https://graph.microsoft.com/.default"
# result = app.acquire_token_interactive(scopes=scopes)
# print(result)
# a = result.get("access_token")
# print(a)

config_data = {
    "authority": f"https://login.microsoftonline.com/{TENANT_ID}",
    "client_id": CLIENT_ID,
    "scope": ["https://"+TENANT_NAME+"/.default"],
    "secret": "<secret value>",
    "endpoint": "https://graph.microsoft.com/v1.0/users"
}

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(
    config_data["client_id"],
    authority=config_data["authority"]
)

result = app.acquire_token_silent(config_data["scope"], account=None, request=auth)
if not result:
    print("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config_data["scope"])
print(result)
a = result.get("access_token")
print(a)


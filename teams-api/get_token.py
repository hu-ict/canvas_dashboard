import msal

CLIENT_ID = "184f1b4a-c0fe-4a81-b680-5eab8c90eeb0"
TENANT_ID = "98932909-9a5a-4d18-ace4-7236b5b5e11d"
RedirectURI = "https://localhost"
tenantname = "hogeschoolutrecht.onmicrosoft.com"

app = msal.PublicClientApplication(
    CLIENT_ID,
    authority="https://login.microsoftonline.com/"+TENANT_ID,
    client_credential=None
)

scopes = ["https://hogeschoolutrecht.onmicrosoft.com/api/read"]

result = app.acquire_token_silent(scopes=scopes, account=tenantname)

print(result["access_token"])

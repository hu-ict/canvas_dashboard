import msal

app = msal.PublicClientApplication(
    CLIENT_ID,
    authority="https://login.microsoftonline.com/"+TENANT_ID,
    client_credential=None
)

scopes = ["https://hogeschoolutrecht.onmicrosoft.com/api/read"]

result = app.acquire_token_silent(scopes=scopes, account=tenantname)

print(result["access_token"])

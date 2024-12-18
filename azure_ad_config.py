import os

AZURE_AD_CONFIG = {
    "CLIENT_ID": os.getenv("AZURE_SECRET_ID"),
    "CLIENT_SECRET": os.getenv("AZURE_CLIENT_SECRET_VALUE"),
    "AUTHORITY": f"https://login.microsoftonline.com/{os.getenv('AZURE_AD_TENANT_ID')}",
    "REDIRECT_URI": "http://localhost:5101/auth/login/callback",
    "SCOPE": ["User.Read"],
}

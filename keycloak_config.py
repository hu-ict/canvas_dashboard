from keycloak.keycloak_openid import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
    server_url="https://iam.web3connect.nl/",
    client_id="flask-client",
    realm_name="canvas_dashboards",
    client_secret_key="UD3yIA4WwRI29vbeB0CigzR1HjPTVQAA"
)

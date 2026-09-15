from authlib.integrations.starlette_client import OAuth 
from app.config import CLIENT_ID,CLIENT_SECRET

oauth = OAuth()
oauth.register(
    name ='google',
    server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration",
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    client_kwargs={
        'scope' : 'email openid profile',
        'redirect_uri':'example/login/auth'
    }
)


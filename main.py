from src.core.di import container
from src.modules.oauth.dto import OAuthCode
from src.usecases.oauth import OAuthLogin
from src.core.constants import GOOGLE_AUTHORIZE_URL

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from src.core.config import config

app = FastAPI()


@app.get('/login')
async def login():
    # Redirect the user to Google's OAuth 2.0 authorization endpoint
    auth_url = (
        f'{GOOGLE_AUTHORIZE_URL}'
        f'?response_type=code'
        f'&client_id={config.google_client_id}'
        f'&redirect_uri={config.redirect_uri}'
        f'&scope=openid email profile'
        f'&access_type=offline'
        f'&prompt=select_account'
    )
    return RedirectResponse(auth_url)


@app.get('/callback')
async def callback(code: str):
    if not code:
        raise HTTPException(status_code=400, detail='Error: No authorization code provided.')

    oauth_login = container.resolve(OAuthLogin)
    access_token, refresh_token = await oauth_login(OAuthCode(code, 'google'))

    return JSONResponse(
        content={
            'message': 'Login successful!',
            'access_token': access_token.value,
            'refresh_token': refresh_token.value,
        }
    )

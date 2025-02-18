from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.responses import (
    JSONResponse,
    RedirectResponse,
)

from src.core.config import config
from src.core.constants import (
    GITHUB_AUTHORIZE_URL,
    GOOGLE_AUTHORIZE_URL,
    OAuthProvider,
)
from src.core.di import container
from src.modules.oauth.dto import OAuthCode
from src.usecases.oauth.login_user import OAuthLogin


app = FastAPI()


@app.get('/oauth/login')
async def oauth_login(provider: OAuthProvider):
    if provider == 'google':
        auth_url = (
            f'{GOOGLE_AUTHORIZE_URL}'
            f'?response_type=code'
            f'&client_id={config.google_client_id}'
            f'&redirect_uri={config.google_redirect_uri}'
            f'&scope=openid email profile'
            f'&access_type=offline'
            f'&prompt=select_account'
        )
    elif provider == 'github':
        auth_url = (
            f'{GITHUB_AUTHORIZE_URL}'
            f'?response_type=code'
            f'&client_id={config.github_client_id}'
            f'&redirect_uri={config.github_redirect_uri}'
            f'&prompt=select_account'
        )
    return RedirectResponse(auth_url)


@app.get('/oauth/callback/google')
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


@app.get('/oauth/callback/github')
async def github_callback(code: str):
    if not code:
        raise HTTPException(status_code=400, detail='Error: No authorization code provided.')

    oauth_login = container.resolve(OAuthLogin)
    access_token, refresh_token = await oauth_login(OAuthCode(code, 'github'))

    return JSONResponse(
        content={
            'message': 'Login successful!',
            'access_token': access_token.value,
            'refresh_token': refresh_token.value,
        }
    )

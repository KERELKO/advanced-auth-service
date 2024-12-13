import typing as t


MFAType = t.Literal['otp', 'code', 'sms', 'auto']
OAuthProvider = t.Literal['github', 'google']

GOOGLE_TOKEN_URL: t.Final[str] = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL: t.Final[str] = 'https://www.googleapis.com/oauth2/v2/userinfo'
GOOGLE_AUTHORIZE_URL: t.Final[str] = 'https://accounts.google.com/o/oauth2/auth'

GITHUB_TOKEN_URL: t.Final[str] = 'https://github.com/login/oauth/access_token'
GITHUB_USER_INFO_URL: t.Final[str] = 'https://api.github.com/user'
GITHUB_AUTHORIZE_URL: t.Final[str] = 'https://github.com/login/oauth/authorize'

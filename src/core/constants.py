import typing as t


MFAType = t.Literal['otp', 'code', 'sms', 'auto']
OAuthProvider = t.Literal['github', 'google']

GOOGLE_TOKEN_URL: t.Final[str] = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL: t.Final[str] = 'https://www.googleapis.com/oauth2/v2/userinfo'
GOOGLE_AUTHORIZE_URL: t.Final[str] = 'https://accounts.google.com/o/oauth2/auth'

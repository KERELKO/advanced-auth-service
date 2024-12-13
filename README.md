# Advanced Auth Service

## Overview
Advanced Auth Service is a authentication solution offering features such as Multi-Factor Authentication (MFA), permission management, and token-based access. It supports user login, registration, and secure access to applications.

## Features
- **User Authentication**: Login and Registration functionalities.
- **Access & Refresh Tokens**: Secure token-based authentication.
- **Multi-Factor Authentication (MFA)**: Supports OTP and email-based verification codes.
- **Permission Logic**: Granular control over user permissions.

## Technologies
- Docker & Docker compose
- Redis
- PostgreSQL
- SQLAlchemy

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Docker & Docker Compose
- Git
- Maketools

### Setup and Run
1. Clone the Repository  
```bash
git clone https://github.com/KERELKO/advanced-auth-service
cd advanced-auth-service/
```
2. Create __.env__ file based on __.env.example__
```bash
cat .env.example > .env
```
3. Build and run docker containers
```bash
docker compose up --build
```

### Usage

#### MFA
OTP MFA requires any authenticator (e.g. Google Authenticator).  
To pass MFA with email code you need to set `APP_EMAIL_ADDRESS` in `.env` file (You can use your own google email)
But to make it work you need to turn on `2-Step Verification` [create password for the app](https://security.google.com/settings/security/apppasswords) and paste this password to `APP_EMAIL_PASSWORD` in `.env` file

#### OAuth2.0
To test __OAuth2.0__ you need to register the app in **Github** or **Google** and have public https url that can serve as `redirect_uri` for the OAuth2.0 provider.
[Google OAuth2.0 documentation](https://support.google.com/cloud/answer/6158849?hl=en)
[GitHub OAuth2.0 documentation](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps)
After registering the application with your chosen service, you will receive a `Client ID` and `Client secret`. Copy these values and add them to `.env` file
```
GOOGLE_CLIENT_ID=google_client_id
GOOGLE_CLIENT_SECRET=google_client_secret

GITHUB_CLIENT_ID=github_client_id
GITHUB_CLIENT_SECRET=github_client_secret
```
Install [tunnelmole](https://tunnelmole.com/) and run with
```
tmole 8000
```
You will see public __http__ and __https__ urls
take the __https__ url and paste it to `OAUTH_REDIRECT_URI` in `.env` file with `/oauth/callback` suffix

Run the application
```
docker compose up
```
In the Browser enter url __`tmole_https_url`/oauth/login?provider=(google or github)__ and pass the OAuth2.0 flow

#### Testing
At the moment app does not expose web API,
and can be tested only with pytest or mock FastAPI endpoints for OAuth2.0

All implemented features tested in `tests` folder.
To run all tests (Including expected input from the user)
```
make tests
```
Run auto tests
```
make auto-tests
```
If you want to run specific test
```
make shell
pytest tests/.../test_you_want_to_run.py
# MFA tests with OTP 
pytest tests/usecases/interactive/test_mfa_with_otp.py
# MFA tests with email code
pytest tests/usecases/interactive/test_mfa_with_email_code.py
```
Inspect all available __Make__ commands in `Makefile`  

## Future Improvements
1. Implement MFA with __Security Token__, __Fingerprint__
2. Implement use cases for:
  - Reset password
  - Forgot password
3. Application OAuth2.0 interface
4. Integrate __roles__ to __permissions__ logic
5. Extend notification services with __PushNotificationService__
6. FastAPI endpoints for use cases
7. Add email verification
8. Celery for notification services

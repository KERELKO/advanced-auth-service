from blacksheep import Application

from . import handlers
from .service import AuthService


def register_module(app: Application):
    app.router.add_post('/api/v1/auth/login', handler=handlers.login_user)
    app.router.add_post('/api/v1/auth/logout', handler=handlers.logout_user)
    app.router.add_post('/api/v1/auth/register', handler=handlers.register_user)

    app.services.register(AuthService)

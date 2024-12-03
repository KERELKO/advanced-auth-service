from blacksheep import Application

from . import handlers
from .service import AuthService


def register_module(app: Application):
    app.router.add_post('/login', handler=handlers.login)
    app.router.add_post('/logout', handler=handlers.logout)
    app.router.add_post('/register', handler=handlers.register)

    app.services.register(AuthService)

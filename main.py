from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info  # type: ignore

from src.core.config import Config
from src.core.di import container
from src.modules.authentication.utils import register_module as register_auth


def app_factory() -> Application:
    config = container.resolve(Config)

    app = Application(services=container)

    register_auth(app)

    if config.env == 'dev':
        app.show_error_details = True

    if config.env in ['dev', 'stage']:
        docs = OpenAPIHandler(
            ui_path='/api/docs',
            info=Info('Advanced Auth API', version='0.0.1'),
        )
        docs.bind_app(app)

    return app

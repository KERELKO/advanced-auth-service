import uvicorn
from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info  # type: ignore

from src.core import config as _config
from src.core.config import Config
from src.core.di import Container
from src.modules.authentication.utils import register_module


def app_factory(config: Config) -> Application:
    app = Application(services=Container())

    app.base_path = '/api'

    register_module(app)

    if config.env == 'dev':
        app.show_error_details = True

    if config.env in ['dev', 'stage']:
        docs = OpenAPIHandler(
            ui_path='/api/docs',
            info=Info('Advanced Auth API', version='0.0.1'),
        )
        docs.bind_app(app)

    return app


if __name__ == '__main__':
    uvicorn.run(app=app_factory(config=_config), host='0.0.0.0', port=8000)

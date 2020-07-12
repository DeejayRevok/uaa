"""
Application main module
"""
import sys

import aiohttp_cors
from aiohttp.web_app import Application
from aiohttp.web_urldispatcher import StaticResource
from aiohttp_apispec import validation_middleware
from news_service_lib import HealthCheck, server_runner

from infrastructure.storage.db_initializer import initialize_db
from infrastructure.storage.sql_storage import SqlStorage
from log_config import LOG_CONFIG, get_logger
from services.authentication_service import AuthService
from services.users_service import UserService
from webapp.definitions import API_VERSION, CONFIG_PATH, health_check
from webapp.middlewares import error_middleware, auth_middleware
from webapp.views import users_view, auth_view


def init_uaa(app: Application) -> Application:
    """
    Initialize the web application

    Args:
        app: configuration profile to use

    Returns: web application initialized
    """
    storage_config = app['config'].get_section('storage')

    store_client = SqlStorage(**storage_config)

    if not store_client.health_check():
        sys.exit(1)

    initialize_db(store_client.engine)
    app['user_service'] = UserService(store_client)
    app['auth_service'] = AuthService(app['user_service'])

    HealthCheck(app, health_check)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })

    users_view.setup_routes(app)
    auth_view.setup_routes(app)

    for route in list(app.router.routes()):
        if not isinstance(route.resource, StaticResource):
            cors.add(route)

    app.middlewares.append(error_middleware)
    app.middlewares.append(auth_middleware)
    app.middlewares.append(validation_middleware)

    return app


if __name__ == '__main__':
    server_runner('UAA', init_uaa, API_VERSION, CONFIG_PATH, LOG_CONFIG, get_logger)

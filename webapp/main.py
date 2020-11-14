"""
Application main module
"""
import sys

from aiohttp.web_app import Application
from aiohttp_apispec import validation_middleware

from models import BASE
from news_service_lib import HealthCheck, server_runner

from log_config import LOG_CONFIG, get_logger
from news_service_lib.storage.sql import create_sql_engine, SqlEngineType, sql_health_check, init_sql_db, \
    SqlSessionProvider
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

    storage_engine = create_sql_engine(SqlEngineType.MYSQL, **storage_config)
    app['storage_engine'] = storage_engine

    init_sql_db(BASE, storage_engine)

    if not sql_health_check(storage_engine):
        sys.exit(1)

    sql_session_provider = SqlSessionProvider(storage_engine)
    app['session_provider'] = sql_session_provider

    app['user_service'] = UserService(sql_session_provider)
    app['auth_service'] = AuthService(app['user_service'])

    HealthCheck(app, health_check)

    users_view.setup_routes(app)
    auth_view.setup_routes(app)

    app.middlewares.append(error_middleware)
    app.middlewares.append(auth_middleware)
    app.middlewares.append(validation_middleware)

    return app


if __name__ == '__main__':
    server_runner('UAA', init_uaa, API_VERSION, CONFIG_PATH, LOG_CONFIG, get_logger)

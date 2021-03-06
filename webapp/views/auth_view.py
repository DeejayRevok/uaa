"""
Authentication views module
"""
from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPBadRequest, HTTPOk
from aiohttp.web_request import Request
from aiohttp.web_response import Response, json_response
from aiohttp_apispec import docs, request_schema
from news_service_lib import ClassRouteTableDef

from log_config import get_logger
from webapp.definitions import API_VERSION
from webapp.request_schemas.auth_request_schemas import PostAuthSchema, PostValidateTokenSchema

ROOT_PATH = '/api/auth'
LOGGER = get_logger()
ROUTES = ClassRouteTableDef()


class AuthViews:
    """
    Authentication REST endpoint views handler
    """

    def __init__(self, app: Application):
        """
        Initialize the authentication views handler

        Args:
            app: application associated
        """
        self.auth_service = app['auth_service']

    @docs(
        tags=['Authentication'],
        summary="Authenticate user",
        description="Authenticate an user by username and password"
    )
    @request_schema(PostAuthSchema)
    @ROUTES.post(f'/{API_VERSION}{ROOT_PATH}')
    async def authenticate(self, request: Request) -> Response:
        """
        Request to authenticate an user

        Args:
            request: input REST request

        Returns: json REST response with the authentication token

        """
        LOGGER.info('REST request to authenticate an user')

        try:
            username = request['data']['username']
            password = request['data']['password']
        except Exception as ex:
            raise HTTPBadRequest(text=str(ex)) from ex

        token_json = await self.auth_service.authenticate(username, password)

        token_response = json_response(token_json, status=200)
        token_response.set_cookie(name='JWT_TOKEN', value=token_json['token'],
                                  httponly='true')
        return token_response

    @docs(
        tags=['Authentication'],
        summary="Logout the authenticated user",
        description="Delete the authentication cookies associated with the request"
    )
    @ROUTES.delete(f'/{API_VERSION}{ROOT_PATH}')
    async def logout(self, _: Request):
        """
        Delete the authorization cookie.

        Args:
            _: input REST request

        Returns: json REST response
        """
        response = HTTPOk()
        response.del_cookie('JWT_TOKEN')
        return response

    @docs(
        tags=['Authentication'],
        summary="Validate token",
        description="Validate JWT token"
    )
    @request_schema(PostValidateTokenSchema)
    @ROUTES.post(f'/{API_VERSION}{ROOT_PATH}/token')
    async def validate_token(self, request: Request) -> Response:
        """
        Request to validate a JWT token

        Args:
            request: input REST request

        Returns: json REST response with the authenticated user data

        """
        LOGGER.info('REST request to validate JWT token')

        try:
            token = request['data']['token']
        except Exception as ex:
            raise HTTPBadRequest(text=str(ex)) from ex

        user = await self.auth_service.validate_token(token)

        return json_response(dict(user), status=200)


def setup_routes(app: Application):
    """
    Add the class routes to the specified application

    Args:
        app: application to add routes

    """
    ROUTES.clean_routes()
    ROUTES.add_class_routes(AuthViews(app))
    app.router.add_routes(ROUTES)

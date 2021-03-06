"""
User views module
"""
from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_request import Request
from aiohttp.web_response import Response, json_response
from aiohttp_apispec import docs, request_schema
from news_service_lib import ClassRouteTableDef, login_required

from log_config import get_logger
from webapp.definitions import API_VERSION
from webapp.request_schemas.user_request_schemas import PostCreateUserSchema

ROOT_PATH = '/api/users'
LOGGER = get_logger()
ROUTES = ClassRouteTableDef()


class UserViews:
    """
    User REST endpoint views handler
    """

    def __init__(self, app: Application):
        """
        Initialize the user views handler

        Args:
            app: application associated
        """
        self.user_service = app['user_service']

    @docs(
        tags=['Users'],
        summary="Get user data",
        description="Get authenticated user data",
        security=[{'ApiKeyAuth': []}]
    )
    @ROUTES.get(f'/{API_VERSION}{ROOT_PATH}/me', allow_head=False)
    async def get_user_data(self, request: Request) -> Response:
        """
        Request to get an user identified by its username

        Args:
            request: input REST request

        Returns: json REST response with the queried user

        """

        @login_required
        async def request_executor(inner_request):
            LOGGER.info('REST request to get one user')

            return json_response(dict(inner_request.user), status=200)

        return await request_executor(request)

    @docs(
        tags=['Users'],
        summary="Create user",
        description="Create a new user"
    )
    @request_schema(PostCreateUserSchema)
    @ROUTES.post(f'/{API_VERSION}{ROOT_PATH}')
    async def post_create_user(self, request: Request) -> Response:
        """
        Request to create an user

        Args:
            request: input REST request

        Returns: json REST response with the created user

        """
        LOGGER.info('REST request to create user')

        try:
            username = request['data']['username']
            password = request['data']['password']
            first_name = request['data']['first_name']
            last_name = request['data']['last_name']
            email = request['data']['email']
        except Exception as ex:
            raise HTTPBadRequest(text=str(ex)) from ex

        user_created = await self.user_service.create_user(username, password, first_name, last_name, email)

        return json_response(dict(user_created), status=200)


def setup_routes(app: Application):
    """
    Add the class routes to the specified application

    Args:
        app: application to add routes

    """
    ROUTES.clean_routes()
    ROUTES.add_class_routes(UserViews(app))
    app.router.add_routes(ROUTES)

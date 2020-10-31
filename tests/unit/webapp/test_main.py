"""
Application entry point test cases
"""
import unittest
from unittest.mock import patch

from aiohttp.web_app import Application
from news_service_lib import Configuration

from services.users_service import UserService
from services.authentication_service import AuthService
from webapp.main import init_uaa


class TestMain(unittest.TestCase):
    """
    Webapp main test cases implementation
    """
    TEST_STORAGE_CONFIG = dict(host='test', port=0, user='test', password='test', database='test')

    # noinspection PyTypeHints
    @patch('webapp.main.sql_health_check')
    @patch('webapp.main.init_sql_db')
    @patch.object(Configuration, 'get_section')
    @patch('webapp.main.users_view')
    @patch('webapp.main.auth_view')
    def test_init_app(self, auth_view_mock, users_view_mock, config_mock, init_sql_mock, health_mock):
        """
        Test if the initialization of the app initializes all the required modules
        """
        health_mock.return_value = True
        config_mock.get_section.return_value = self.TEST_STORAGE_CONFIG
        base_app = Application()
        base_app['config'] = config_mock
        app = init_uaa(base_app)
        auth_view_mock.setup_routes.assert_called_once()
        users_view_mock.setup_routes.assert_called_once()
        init_sql_mock.assert_called_once()
        self.assertIsNotNone(app['user_service'])
        self.assertIsNotNone(app['auth_service'])
        self.assertTrue(isinstance(app['user_service'], UserService))
        self.assertTrue(isinstance(app['auth_service'], AuthService))
        self.assertEqual(app['auth_service']._user_service, app['user_service'])

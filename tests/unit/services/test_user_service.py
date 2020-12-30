"""
User service test cases
"""
import asyncio
from unittest import TestCase
from unittest.mock import patch, MagicMock

from models.user import User
from services.users_service import UserService

TEST_USERNAME = 'test_user'
TEST_PASSWORD = 'Test1@34'
TEST_FIRST_NAME = 'test_first_name'
TEST_LAST_NAME = 'test_last_name'
TEST_EMAIL = 'test@test.com'


class TestUserService(TestCase):
    """
    User service test cases
    """

    @patch('services.users_service.storage_factory')
    def setUp(self, factory_mock):
        """
        Set up each test environment
        """
        self.client_mock = MagicMock()
        factory_mock.return_value = self.client_mock
        self.user_service = UserService(MagicMock())

    def test_create_user(self):
        """
        Chech if the create user service calls to the storage client persist method
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(
            self.user_service.create_user(TEST_USERNAME, TEST_PASSWORD, TEST_FIRST_NAME, TEST_LAST_NAME, TEST_EMAIL))
        self.client_mock.save.assert_called_once()
        self.assertEqual(self.client_mock.save.call_args[0][0].username, TEST_USERNAME)

    def test_get_user_id(self):
        """
        Check if the get user by id method returns the stored instance
        """
        loop = asyncio.new_event_loop()
        self.client_mock.get_one.return_value = User(username=TEST_USERNAME, password=TEST_PASSWORD)
        result = loop.run_until_complete(self.user_service.get_user_by_id(1))
        self.assertEqual(result.username, TEST_USERNAME)

    def test_get_user_name(self):
        """
        Check if the get user by name method returns the stored instance
        """
        loop = asyncio.new_event_loop()
        self.client_mock.get_one.return_value = User(username=TEST_USERNAME, password=TEST_PASSWORD)
        result = loop.run_until_complete(self.user_service.get_user_by_name(TEST_USERNAME))
        self.assertEqual(result.username, TEST_USERNAME)

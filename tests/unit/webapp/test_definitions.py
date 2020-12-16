"""
Test for the definitions module functions
"""
import unittest
from unittest.mock import patch, MagicMock

from aiohttp.web_app import Application
from aiounittest import async_test

from webapp.definitions import health_check


class TestDefinitions(unittest.TestCase):
    """
    Test case for definitions module
    """
    TEST_STORAGE_CONFIG = dict(host='test', port=0, user='test', password='test', schema='test')

    @patch('webapp.definitions.sql_health_check')
    @async_test
    async def test_healthcheck(self, health_check_mock):
        """
        Test the app healthcheck method
        """
        app = Application()
        engine_mock = MagicMock()
        app['storage_engine'] = engine_mock
        health_check_mock.return_value = True
        health = await health_check(app)
        self.assertTrue(health)
        health_check_mock.assert_called_with(engine_mock)

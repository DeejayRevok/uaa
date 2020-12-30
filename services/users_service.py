"""
Users service module
"""
from news_service_lib.storage import StorageError, storage_factory, StorageType
from news_service_lib.storage.filter import MatchFilter
from news_service_lib.storage.sql import SqlSessionProvider

from models import User
from log_config import get_logger

LOGGER = get_logger()


class UserService:
    """
    User service implementation
    """

    def __init__(self, session_provider: SqlSessionProvider):
        """
        Initialize the user service with the specified session provider

        Args:
            session_provider: database sql sessions provider
        """
        self._repo = storage_factory(StorageType.SQL.value, dict(session_provider=session_provider, model=User),
                                     logger=LOGGER)

    async def create_user(self, username: str, password: str, first_name: str, last_name: str, email: str) -> User:
        """
        Create a new user

        Args:
            username: user name
            password: user password
            first_name: user's first name
            last_name: user's last name
            email: user's email address

        Returns: user model created

        """
        try:
            return self._repo.save(
                User(username=username, password=password, first_name=first_name, last_name=last_name,
                     email=email))
        except StorageError:
            raise ValueError(f'User already exists')

    async def get_user_by_id(self, identifier: int) -> User:
        """
        Get an user by its identifier

        Args:
            identifier: user identifier to get

        Returns: queried user

        """
        return self._repo.get_one(filters=[MatchFilter('id', identifier)])

    async def get_user_by_name(self, username: str) -> User:
        """
        Gets an user by its name

        Args:
            username: user name to get

        Returns: queried user

        """
        return self._repo.get_one(filters=[MatchFilter('username', username)])

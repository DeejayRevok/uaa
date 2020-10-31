"""
Users service module
"""
from sqlalchemy.engine import Engine

from news_service_lib.storage import StorageError, storage_factory, StorageType
from news_service_lib.storage.filter import MatchFilter

from lib.pass_tools import hash_password
from models import User
from log_config import get_logger

LOGGER = get_logger()


class UserService:
    """
    User service implementation
    """

    def __init__(self, db_engine: Engine):
        """
        Initialize the user service with the specified database engine

        Args:
            db_engine: database engine
        """
        self._repo = storage_factory(StorageType.SQL.value, dict(engine=db_engine, model=User), logger=LOGGER)

    async def create_user(self, username: str, password: str) -> User:
        """
        Create a new user

        Args:
            username: user name
            password: user password

        Returns: user model created

        """
        password_hash = hash_password(password)
        try:
            return self._repo.save(User(username=username, password=password_hash))
        except StorageError:
            raise ValueError(f'User {username} already exists')

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

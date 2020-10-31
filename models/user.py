"""
User model module
"""
from sqlalchemy import Column, Integer, String

from models.base import BASE


class User(BASE):
    """
    User model
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))

    def __iter__(self) -> iter:
        """
        Iterate over the model properties

        Returns: iterator to the model properties

        """
        yield 'id', self.id
        yield 'username', self.username

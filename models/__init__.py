"""
Database models initialization module
"""
from models.base import BASE
from models.user import User

__all__ = [
    "BASE",
    "User"
]

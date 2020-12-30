"""
User model module
"""
from email_validator import validate_email
from password_validator import PasswordValidator
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from lib.pass_tools import hash_password
from models.base import BASE

# Password valid schema
password_schema = PasswordValidator().min(8).max(
    100).has().uppercase().has().lowercase().has().digits().has().symbols().has().no().spaces()


class User(BASE):
    """
    User model
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(255))
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    @validates('username')
    def validate_username(self, key: str, value: str):
        """
        Validate the username value

        Args:
            key: key of the column to validate
            value: value to validate

        Returns: validated value

        """
        if not len(value.strip()):
            raise ValueError(f'Invalid value for {key} field')
        return value

    @validates('password')
    def validate_password(self, _: str, value: str):
        """
        Validate the password value

        Args:
            _: key of the column to validate
            value: value to validate

        Returns: validated password hash

        """
        if password_schema.validate(value):
            return hash_password(value)
        else:
            raise ValueError("The password should contain uppercase and lowercase letters, digits, symbols "
                             "and no spaces. Minimum password length is 8, maximum is 100")

    @validates('email')
    def validates_email(self, _: str, value: str):
        """
        Validate the email value

        Args:
            _: key of the column to validate
            value: value to validate

        Returns: validated value

        """
        return validate_email(value).email

    def __iter__(self) -> iter:
        """
        Iterate over the model properties

        Returns: iterator to the model properties

        """
        yield 'id', self.id
        yield 'username', self.username
        yield 'first_name', self.first_name
        yield 'last_name', self.last_name
        yield 'email', self.email

"""
User request schemas module
"""
from marshmallow import Schema, fields


class PostCreateUserSchema(Schema):
    """
    Class that describes the schema of the post create user request
    """
    username = fields.Str(description="User username")
    password = fields.Str(description="User password")
    first_name = fields.Str(description="First user name")
    last_name = fields.Str(description="Last user name")
    email = fields.Str(description="User email address")

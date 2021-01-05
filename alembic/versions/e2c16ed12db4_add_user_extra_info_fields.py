"""Add User Extra Info Fields

Revision ID: e2c16ed12db4
Revises: 
Create Date: 2020-12-30 20:42:01.825189

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import Column, DefaultClause

revision = 'e2c16ed12db4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', Column('first_name', sa.String(255), DefaultClause(""), nullable=False))
    op.add_column('users', Column('last_name', sa.String(255), DefaultClause(""), nullable=False))
    op.add_column('users', Column('email', sa.String(255), DefaultClause(""), nullable=False))


def downgrade():
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'email')

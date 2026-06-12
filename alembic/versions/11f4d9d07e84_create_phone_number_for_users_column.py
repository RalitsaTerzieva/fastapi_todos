"""Create phone number for users column

Revision ID: 11f4d9d07e84
Revises: 
Create Date: 2026-06-11 19:03:43.102700

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11f4d9d07e84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')

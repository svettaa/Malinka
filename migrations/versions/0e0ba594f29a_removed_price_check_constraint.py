"""Removed price check constraint

Revision ID: 0e0ba594f29a
Revises: e8c69831d42b
Create Date: 2020-05-04 18:16:26.974808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e0ba594f29a'
down_revision = 'e8c69831d42b'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('price_max_greater_min', 'procedure', type_='check')


def downgrade():
    op.create_check_constraint('price_max_greater_min', 'procedure', 'price_max IS NULL OR price_max > price_min')

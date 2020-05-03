"""Price check constraint

Revision ID: 6d3956699398
Revises: 328ecb2f2c6a
Create Date: 2020-05-01 19:53:18.142428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d3956699398'
down_revision = '328ecb2f2c6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_check_constraint('price_max_greater_min', 'procedure', 'price_max IS NULL OR price_max > price_min')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('price_max_greater_min', 'procedure', type_='check')
    # ### end Alembic commands ###
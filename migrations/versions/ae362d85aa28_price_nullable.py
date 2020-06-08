"""price nullable

Revision ID: ae362d85aa28
Revises: c5007c2e3099
Create Date: 2020-06-03 22:10:32.286534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae362d85aa28'
down_revision = 'c5007c2e3099'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointment', 'price',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointment', 'price',
               existing_type=sa.NUMERIC(precision=14, scale=2),
               nullable=False)
    # ### end Alembic commands ###
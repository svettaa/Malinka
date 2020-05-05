"""Removed time from schedule change

Revision ID: 408e599d5164
Revises: 0e0ba594f29a
Create Date: 2020-05-05 23:35:23.153171

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '408e599d5164'
down_revision = '0e0ba594f29a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedule_change', 'change_start')
    op.drop_column('schedule_change', 'change_end')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule_change', sa.Column('change_end', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('schedule_change', sa.Column('change_start', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###

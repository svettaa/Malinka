"""first name Client

Revision ID: 3cfada6ad5d7
Revises: 967f8a6f84a6
Create Date: 2020-04-29 18:58:30.962830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cfada6ad5d7'
down_revision = '967f8a6f84a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('first_name', sa.String(length=20), nullable=False))
    op.drop_column('client', 'fist_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('fist_name', sa.VARCHAR(length=20), autoincrement=False, nullable=False))
    op.drop_column('client', 'first_name')
    # ### end Alembic commands ###

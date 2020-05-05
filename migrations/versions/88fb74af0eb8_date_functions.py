"""date functions

Revision ID: 88fb74af0eb8
Revises: 0e0ba594f29a
Create Date: 2020-05-05 09:33:01.975083

"""
from alembic import op
import sqlalchemy as sa

from app.alembic_op import ReplaceableObject

# revision identifiers, used by Alembic.
revision = '88fb74af0eb8'
down_revision = '0e0ba594f29a'
branch_labels = None
depends_on = None

is_future_date = ReplaceableObject(
    'is_future_date_and_time(param_date date, param_time time)',
    """
   RETURNS boolean AS $$
   BEGIN
       RETURN param_date > CURRENT_DATE OR
              (param_date = CURRENT_DATE AND param_time > CURRENT_TIME);
   END;
   $$ LANGUAGE plpgsql;
   """
)

is_even_day = ReplaceableObject(
    'is_even_day(param_date date)',
    """
   RETURNS boolean AS $$
   BEGIN
       RETURN (CAST(EXTRACT(DAY FROM param_date) AS INTEGER) % 2 = 0);
   END;
   $$ LANGUAGE plpgsql;
   """
)


def upgrade():
    op.create_sp(is_future_date)
    op.create_sp(is_even_day)


def downgrade():
    op.drop_sp(is_future_date)
    op.drop_sp(is_even_day)

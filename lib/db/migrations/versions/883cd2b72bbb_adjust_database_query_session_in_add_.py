"""adjust database query session in add_user and add_transaction

Revision ID: 883cd2b72bbb
Revises: 799b157adf58
Create Date: 2024-03-23 20:56:41.260092

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '883cd2b72bbb'
down_revision: Union[str, None] = '799b157adf58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
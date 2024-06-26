"""adjusting relationships in transaction and category tables

Revision ID: 376111dc4c85
Revises: 9ba8c4a26097
Create Date: 2024-03-25 12:52:50.712574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '376111dc4c85'
down_revision: Union[str, None] = '9ba8c4a26097'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transaction', 'categories', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.drop_column('transaction', 'category_id')
    # ### end Alembic commands ###

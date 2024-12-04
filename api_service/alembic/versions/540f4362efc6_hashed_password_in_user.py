"""hashed_password_in_User

Revision ID: 540f4362efc6
Revises: 49ff7050a326
Create Date: 2024-12-05 00:26:01.375041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '540f4362efc6'
down_revision: Union[str, None] = '49ff7050a326'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userprofile', sa.Column('hashing_password', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'userprofile', ['username'])
    op.drop_column('userprofile', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userprofile', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'userprofile', type_='unique')
    op.drop_column('userprofile', 'hashing_password')
    # ### end Alembic commands ###

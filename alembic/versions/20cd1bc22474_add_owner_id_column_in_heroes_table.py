"""Add owner_id column in heroes table

Revision ID: 20cd1bc22474
Revises: 
Create Date: 2026-05-25 10:44:23.670597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20cd1bc22474'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('heroes', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_heroes_owner_id_players",
        "heroes", # source table
        "players", # target table
        ['owner_id'], # source column
        ['id'] # target column
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_heroes_owner_id_players", "heroes", type_='foreignkey')
    op.drop_column('heroes', 'owner_id')

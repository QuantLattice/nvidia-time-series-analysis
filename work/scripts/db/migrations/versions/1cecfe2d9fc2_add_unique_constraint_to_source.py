"""add unique constraint to source

Revision ID: 1cecfe2d9fc2
Revises: 3958b871ea85
Create Date: 2026-05-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = '1cecfe2d9fc2'
down_revision: Union[str, Sequence[str], None] = '3958b871ea85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        'uq_stock_quotes_source',
        'stock_quotes',
        ['source'],
    )


def downgrade() -> None:
    op.drop_constraint(
        'uq_stock_quotes_source',
        'stock_quotes',
        type_='unique',
    )

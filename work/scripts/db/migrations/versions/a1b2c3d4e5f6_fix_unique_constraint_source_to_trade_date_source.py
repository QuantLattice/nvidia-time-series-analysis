"""fix unique constraint: replace source-only with (trade_date, source)

Revision ID: a1b2c3d4e5f6
Revises: 1cecfe2d9fc2
Create Date: 2026-06-12 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '1cecfe2d9fc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        'uq_stock_quotes_source',
        'stock_quotes',
        type_='unique',
    )
    op.create_unique_constraint(
        'uq_stock_quotes_trade_date_source',
        'stock_quotes',
        ['trade_date', 'source'],
    )


def downgrade() -> None:
    op.drop_constraint(
        'uq_stock_quotes_trade_date_source',
        'stock_quotes',
        type_='unique',
    )
    op.create_unique_constraint(
        'uq_stock_quotes_source',
        'stock_quotes',
        ['source'],
    )

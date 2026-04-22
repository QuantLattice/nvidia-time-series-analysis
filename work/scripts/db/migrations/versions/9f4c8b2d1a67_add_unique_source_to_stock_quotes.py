"""add unique source to stock quotes

Revision ID: 9f4c8b2d1a67
Revises: 14128badc72a
Create Date: 2026-04-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f4c8b2d1a67"
down_revision: Union[str, Sequence[str], None] = "14128badc72a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "stock_quotes",
        sa.Column("source", sa.String(length=512), nullable=True),
    )
    op.execute("UPDATE stock_quotes SET source = CONCAT('legacy:', id)")
    op.alter_column(
        "stock_quotes",
        "source",
        existing_type=sa.String(length=512),
        nullable=False,
    )
    op.create_unique_constraint(
        op.f("uq_stock_quotes_source"),
        "stock_quotes",
        ["source"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        op.f("uq_stock_quotes_source"),
        "stock_quotes",
        type_="unique",
    )
    op.drop_column("stock_quotes", "source")

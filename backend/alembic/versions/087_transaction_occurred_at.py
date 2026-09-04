"""store Open Finance clock time on transactions, seconds precision

Revision ID: 087
Revises: 086
Create Date: 2026-09-04
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "087"
down_revision: Union[str, None] = "086"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "transactions",
        sa.Column(
            "occurred_at",
            postgresql.TIMESTAMP(timezone=True, precision=0),
            nullable=True,
        ),
    )
    op.execute(
        """
        UPDATE transactions
        SET occurred_at = date_trunc(
            'second',
            (raw_data->>'date')::timestamptz
        )
        WHERE raw_data IS NOT NULL
          AND jsonb_typeof(raw_data->'date') = 'string'
          AND raw_data->>'date' ~ '[Tt ][0-9]'
        """
    )


def downgrade() -> None:
    op.drop_column("transactions", "occurred_at")

"""Alter events.datetime to timezone aware

Revision ID: 96f4b42aaf43
Revises: 5cb970b762f8
Create Date: 2025-07-15 17:58:07.114072

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "96f4b42aaf43"
down_revision: Union[str, Sequence[str], None] = "5cb970b762f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "events",
        "datetime",
        type_=sa.DateTime(timezone=True),
        postgresql_using="datetime AT TIME ZONE 'UTC'",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("events", "datetime", type_=sa.DateTime(timezone=False))

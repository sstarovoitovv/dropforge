"""create drops

Revision ID: 0aa5662dde1a
Revises: 
Create Date: 2026-09-21 20:51:08.698257

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '0aa5662dde1a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE drops (
            id UUID PRIMARY KEY,
            content TEXT NOT NULL,
            expires_at TIMESTAMPTZ,
            views_remaining INTEGER
        );
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE drops;")
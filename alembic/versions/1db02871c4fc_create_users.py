"""create users

Revision ID: 1db02871c4fc
Revises: 0aa5662dde1a
Create Date: 2026-09-22 20:31:02.118701

"""
from typing import Sequence, Union

from alembic import op



# revision identifiers, used by Alembic.
revision: str = '1db02871c4fc'
down_revision: Union[str, Sequence[str], None] = '0aa5662dde1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE users (
            id UUID PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE users;")
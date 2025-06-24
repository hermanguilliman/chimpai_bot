"""add shared token field

Revision ID: 6e98e3fcd6fa
Revises: 5e5472ae1acf
Create Date: 2025-06-24 22:13:28.211815

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6e98e3fcd6fa"
down_revision: Union[str, None] = "5e5472ae1acf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "custom_personality",
        sa.Column(
            "shared_token",
            sa.String(length=36),
            nullable=True,
            unique=True,
            index=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("custom_personality", "shared_token")

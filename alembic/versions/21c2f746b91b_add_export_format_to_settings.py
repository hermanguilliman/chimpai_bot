"""Add export_format to settings

Revision ID: 21c2f746b91b
Revises: f8c51ba1b100
Create Date: 2025-06-15 13:40:46.444887

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "21c2f746b91b"
down_revision: Union[str, None] = "f8c51ba1b100"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "settings",
        sa.Column(
            "export_format",
            sa.String(10),
            nullable=False,
            server_default="markdown",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("settings", "export_format")

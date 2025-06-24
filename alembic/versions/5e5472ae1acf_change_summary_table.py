"""change summary table

Revision ID: 5e5472ae1acf
Revises: 65fd1674af3d
Create Date: 2025-06-24 11:25:59.453072

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5e5472ae1acf"
down_revision: Union[str, None] = "65fd1674af3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем новый столбец summary_size
    op.add_column(
        "summary_settings",
        sa.Column(
            "summary_type",
            sa.String(10),
            nullable=False,
            server_default="detailed",
        ),
    )
    # Удаляем старый столбец export_format
    op.drop_column("summary_settings", "export_format")


def downgrade() -> None:
    """Downgrade schema."""
    # Добавляем обратно столбец export_format
    op.add_column(
        "summary_settings",
        sa.Column(
            "export_format",
            sa.String(10),
            nullable=False,
            server_default="markdown",
        ),
    )
    # Удаляем столбец summary_size
    op.drop_column("summary_settings", "summary_size")

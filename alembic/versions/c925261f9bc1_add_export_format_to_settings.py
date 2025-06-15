"""Add export_format to settings

Revision ID: c925261f9bc1
Revises: 21c2f746b91b
Create Date: 2025-06-15 13:48:54.960264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c925261f9bc1'
down_revision: Union[str, None] = '21c2f746b91b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""add content column

Revision ID: ffaee2d49963
Revises: 8e7ba756fc6a
Create Date: 2026-10-08 14:49:35.643864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ffaee2d49963'
down_revision: Union[str, Sequence[str], None] = '1c569e5818af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

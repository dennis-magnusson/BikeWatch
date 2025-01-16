"""add category property

Revision ID: 0294a402e296
Revises: 7e03de24a0ca
Create Date: 2025-01-16 19:12:27.799360

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0294a402e296"
down_revision: Union[str, None] = "7e03de24a0ca"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("bike", sa.Column("category", sa.String))


def downgrade() -> None:
    op.drop_column("bike", "category")

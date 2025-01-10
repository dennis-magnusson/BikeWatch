"""add_bike_size_type_column

Revision ID: 7e03de24a0ca
Revises: 6f3f7420df48
Create Date: 2025-01-10 15:59:50.237833

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7e03de24a0ca"
down_revision: Union[str, None] = "6f3f7420df48"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("bike", sa.Column("letter_size_min", sa.String(), nullable=True))
    op.add_column("bike", sa.Column("number_size_min", sa.Float(), nullable=True))
    op.add_column("bike", sa.Column("letter_size_max", sa.String(), nullable=True))
    op.add_column("bike", sa.Column("number_size_max", sa.Float(), nullable=True))
    op.drop_column("bike", "size")


def downgrade() -> None:
    op.drop_column("bike", "number_size_min")
    op.drop_column("bike", "letter_size_min")
    op.drop_column("bike", "number_size_max")
    op.drop_column("bike", "letter_size_max")
    op.add_column("bike", sa.Column("size", sa.String(), nullable=True))

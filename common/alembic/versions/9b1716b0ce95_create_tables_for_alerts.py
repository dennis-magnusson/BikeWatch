"""create tables for alerts

Revision ID: 9b1716b0ce95
Revises: 0294a402e296
Create Date: 2025-01-23 19:59:07.384502

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9b1716b0ce95"
down_revision: Union[str, None] = "0294a402e296"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_alert",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "chat_id",
            sa.String(),
        ),
        sa.Column("min_price", sa.Float()),
        sa.Column("max_price", sa.Float()),
        sa.Column("category", sa.String()),
        sa.Column("city", sa.String()),
        sa.Column("region", sa.String()),
        sa.Column("size", sa.Float()),
        sa.Column("size_flexibility", sa.Boolean()),
    )

    op.create_table(
        "alerted_listing",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("alert_id", sa.Integer(), sa.ForeignKey("user_alert.id")),
        sa.Column("listing_id", sa.Integer(), sa.ForeignKey("bike_listing.id")),
    )


def downgrade() -> None:
    op.drop_table("alerted_listing")
    op.drop_table("user_alert")

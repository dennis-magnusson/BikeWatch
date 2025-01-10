"""create_bike_and_bike_image_tables

Revision ID: 6f3f7420df48
Revises: 
Create Date: 2025-01-10 15:51:45.981226

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6f3f7420df48'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bike",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("brand", sa.String),
        sa.Column("model", sa.String),
        sa.Column("year", sa.Integer),
        sa.Column("url", sa.String, nullable=False),
        sa.Column("date_posted", sa.DateTime),
        sa.Column("size", sa.String),
        sa.Column("price", sa.Float),
        sa.Column("city", sa.String),
        sa.Column("region", sa.String),
        sa.Column("description", sa.String),
        sa.Column("short_description", sa.String),
    )

    op.create_table(
        "bike_image",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("bike_id", sa.Integer, sa.ForeignKey("bike.id")),
        sa.Column("url", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("bikes")
    op.drop_table("bike_image")

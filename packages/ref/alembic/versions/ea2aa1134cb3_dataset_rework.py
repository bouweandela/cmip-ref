"""dataset-rework

Revision ID: ea2aa1134cb3
Revises:
Create Date: 2024-11-20 21:34:38.183261

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ea2aa1134cb3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "dataset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("dataset_type", sa.Enum("CMIP6", "CMIP7", name="sourcedatasettype"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_table(
        "cmip6_dataset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.String(), nullable=False),
        sa.Column("branch_method", sa.String(), nullable=False),
        sa.Column("branch_time_in_child", sa.Float(), nullable=False),
        sa.Column("branch_time_in_parent", sa.Float(), nullable=False),
        sa.Column("experiment", sa.String(), nullable=False),
        sa.Column("experiment_id", sa.String(), nullable=False),
        sa.Column("frequency", sa.String(), nullable=False),
        sa.Column("grid", sa.String(), nullable=False),
        sa.Column("grid_label", sa.String(), nullable=False),
        sa.Column("init_year", sa.Integer(), nullable=True),
        sa.Column("institution_id", sa.String(), nullable=False),
        sa.Column("long_name", sa.String(), nullable=False),
        sa.Column("member_id", sa.String(), nullable=False),
        sa.Column("nominal_resolution", sa.String(), nullable=False),
        sa.Column("parent_activity_id", sa.String(), nullable=False),
        sa.Column("parent_experiment_id", sa.String(), nullable=False),
        sa.Column("parent_source_id", sa.String(), nullable=False),
        sa.Column("parent_time_units", sa.String(), nullable=False),
        sa.Column("parent_variant_label", sa.String(), nullable=False),
        sa.Column("realm", sa.String(), nullable=False),
        sa.Column("product", sa.String(), nullable=False),
        sa.Column("source_id", sa.String(), nullable=False),
        sa.Column("standard_name", sa.String(), nullable=False),
        sa.Column("source_type", sa.String(), nullable=False),
        sa.Column("sub_experiment", sa.String(), nullable=False),
        sa.Column("sub_experiment_id", sa.String(), nullable=False),
        sa.Column("table_id", sa.String(), nullable=False),
        sa.Column("units", sa.String(), nullable=False),
        sa.Column("variable_id", sa.String(), nullable=False),
        sa.Column("variant_label", sa.String(), nullable=False),
        sa.Column("vertical_levels", sa.Integer(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("instance_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"],
            ["dataset.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cmip6_dataset_file",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("dataset_id", sa.Integer(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=True),
        sa.Column("path", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["dataset_id"], ["cmip6_dataset.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cmip6_dataset_file")
    op.drop_table("cmip6_dataset")
    op.drop_table("dataset")
    # ### end Alembic commands ###
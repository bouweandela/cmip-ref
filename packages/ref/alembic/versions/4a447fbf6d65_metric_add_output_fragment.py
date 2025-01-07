"""metric_add_output_fragment

Revision ID: 4a447fbf6d65
Revises: 4b95a617184e
Create Date: 2024-12-19 12:16:38.605113

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4a447fbf6d65"
down_revision: Union[str, None] = "4b95a617184e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("metric_execution_result", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "output_fragment",
                sa.String(),
                nullable=False,
                default="",  # This is the default value for the migration
            )
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("metric_execution_result", schema=None) as batch_op:
        batch_op.drop_column("output_fragment")

    # ### end Alembic commands ###
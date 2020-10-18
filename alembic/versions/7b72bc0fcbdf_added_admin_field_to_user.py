"""added admin field to user

Revision ID: 7b72bc0fcbdf
Revises: 8fcf94da1a41
Create Date: 2020-10-18 12:16:31.799518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b72bc0fcbdf'
down_revision = '8fcf94da1a41'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column('admin', sa.Boolean(), nullable=True, default=False))


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("admin")

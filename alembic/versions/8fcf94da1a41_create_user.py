"""create user

Revision ID: 8fcf94da1a41
Revises: 
Create Date: 2020-10-16 17:46:50.013822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fcf94da1a41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('hashed_google_id', sa.String(), nullable=True),
                    sa.Column('token', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_hashed_google_id'), 'users', ['hashed_google_id'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_hashed_google_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###

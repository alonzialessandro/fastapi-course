"""add last fews columns to posts table

Revision ID: 2ec540bf1df0
Revises: 067ac6508b0e
Create Date: 2023-01-31 18:46:16.521038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ec540bf1df0'
down_revision = '067ac6508b0e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    pass

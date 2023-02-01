"""add content column to post table

Revision ID: c43fb99efb8b
Revises: b976a71876a3
Create Date: 2023-01-31 18:07:24.745737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c43fb99efb8b'
down_revision = 'b976a71876a3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass

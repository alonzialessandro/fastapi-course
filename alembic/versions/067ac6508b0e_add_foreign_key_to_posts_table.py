"""add foreign-key to posts table

Revision ID: 067ac6508b0e
Revises: a6d15928d6be
Create Date: 2023-01-31 18:33:02.462808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '067ac6508b0e'
down_revision = 'a6d15928d6be'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', 
        local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass

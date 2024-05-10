"""Add image_file column to Post model

Revision ID: 1d9b871877a9
Revises: e7d920cdf780
Create Date: 2024-05-05 18:30:23.353732

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic
revision = '1d9b871877a9'
down_revision = 'e7d920cdf780'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_file', sa.String(length=50), nullable=False, server_default='default.jpg'))

def downgrade():
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('image_file')


    # ### end Alembic commands ###

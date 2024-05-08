"""Added description column to books table

Revision ID: e7d920cdf780
Revises: 
Create Date: 2024-05-04 14:25:20.426616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7d920cdf780'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=255), nullable=True))
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)
        batch_op.alter_column('title',
               existing_type=sa.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('genre',
               existing_type=sa.TEXT(),
               type_=sa.String(length=120),
               existing_nullable=True)
        batch_op.alter_column('author',
               existing_type=sa.TEXT(),
               type_=sa.String(length=120),
               nullable=True)
        batch_op.alter_column('status',
               existing_type=sa.TEXT(),
               type_=sa.String(length=50),
               existing_nullable=True)
        batch_op.alter_column('isbn',
               existing_type=sa.TEXT(),
               type_=sa.String(length=20),
               existing_nullable=True)
        batch_op.drop_column('publication_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('publication_date', sa.TEXT(), nullable=True))
        batch_op.alter_column('isbn',
               existing_type=sa.String(length=20),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('status',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('author',
               existing_type=sa.String(length=120),
               type_=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('genre',
               existing_type=sa.String(length=120),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.String(length=255),
               type_=sa.TEXT(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
        batch_op.drop_column('description')

    # ### end Alembic commands ###

"""add table

Revision ID: ecbf1408f5e1
Revises: 7de5447d59dc
Create Date: 2023-12-19 21:00:06.701399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecbf1408f5e1'
down_revision = '7de5447d59dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_brands',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('brand_name', sa.String(length=225), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('product_brands', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_product_brands_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_product_brands_updated_at'), ['updated_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_brands', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_product_brands_updated_at'))
        batch_op.drop_index(batch_op.f('ix_product_brands_created_at'))

    op.drop_table('product_brands')
    # ### end Alembic commands ###

"""add table

Revision ID: 0634df2780ae
Revises: ecbf1408f5e1
Create Date: 2023-12-19 21:01:35.389243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0634df2780ae'
down_revision = 'ecbf1408f5e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_catalogs',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('product_name', sa.String(length=225), nullable=False),
    sa.Column('type', sa.String(length=225), nullable=False),
    sa.Column('brand_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['product_brands.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('product_catalogs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_product_catalogs_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_product_catalogs_updated_at'), ['updated_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_catalogs', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_product_catalogs_updated_at'))
        batch_op.drop_index(batch_op.f('ix_product_catalogs_created_at'))

    op.drop_table('product_catalogs')
    # ### end Alembic commands ###

"""delete objecthouse table

Revision ID: 6bd24081fd96
Revises: e40eb2bb2129
Create Date: 2019-10-14 17:31:40.785347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bd24081fd96'
down_revision = 'e40eb2bb2129'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('object_house')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('object_house',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('developer_id', sa.INTEGER(), nullable=True),
    sa.Column('housing_complex_id', sa.INTEGER(), nullable=True),
    sa.Column('house_id', sa.INTEGER(), nullable=True),
    sa.Column('room', sa.INTEGER(), nullable=True),
    sa.Column('square', sa.FLOAT(), nullable=True),
    sa.Column('price', sa.FLOAT(), nullable=True),
    sa.Column('price_meter', sa.FLOAT(), nullable=True),
    sa.Column('floor', sa.INTEGER(), nullable=True),
    sa.Column('floor_number', sa.INTEGER(), nullable=True),
    sa.Column('house_number', sa.INTEGER(), nullable=True),
    sa.Column('section_number', sa.INTEGER(), nullable=True),
    sa.Column('type_studio', sa.VARCHAR(length=16), nullable=True),
    sa.Column('type', sa.VARCHAR(length=32), nullable=True),
    sa.Column('decoration', sa.VARCHAR(length=16), nullable=True),
    sa.Column('price_discont', sa.FLOAT(), nullable=True),
    sa.Column('source', sa.VARCHAR(length=128), nullable=True),
    sa.Column('house_name', sa.VARCHAR(length=128), nullable=True),
    sa.ForeignKeyConstraint(['developer_id'], ['developer.id'], ),
    sa.ForeignKeyConstraint(['house_id'], ['house.id'], ),
    sa.ForeignKeyConstraint(['housing_complex_id'], ['housing_complex.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
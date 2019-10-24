"""add DateComplete

Revision ID: 210cf617e787
Revises: 6531757181e8
Create Date: 2019-10-23 20:20:58.347989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '210cf617e787'
down_revision = '6531757181e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('date_complete',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('dt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('date_complete')
    # ### end Alembic commands ###
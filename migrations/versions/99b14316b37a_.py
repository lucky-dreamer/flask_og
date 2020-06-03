"""empty message

Revision ID: 99b14316b37a
Revises: c5fd5bf1a9dd
Create Date: 2020-04-30 11:14:03.728416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99b14316b37a'
down_revision = 'c5fd5bf1a9dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_inform', sa.Column('time', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tb_inform', 'time')
    # ### end Alembic commands ###

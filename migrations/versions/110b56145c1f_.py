"""empty message

Revision ID: 110b56145c1f
Revises: 137c1343020a
Create Date: 2020-04-09 10:56:53.930119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '110b56145c1f'
down_revision = '137c1343020a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_student', sa.Column('is_sign', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tb_student', 'is_sign')
    # ### end Alembic commands ###

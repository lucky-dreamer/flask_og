"""empty message

Revision ID: ba8ea9fd5b6f
Revises: 5b2c7cca05e4
Create Date: 2020-04-03 15:12:52.384169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba8ea9fd5b6f'
down_revision = '5b2c7cca05e4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_student', sa.Column('grade', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tb_student', 'grade')
    # ### end Alembic commands ###

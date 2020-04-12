"""empty message

Revision ID: 54d82fa8fead
Revises: ba8ea9fd5b6f
Create Date: 2020-04-08 17:06:31.126793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54d82fa8fead'
down_revision = 'ba8ea9fd5b6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_student', sa.Column('sign_times', sa.Integer(), nullable=True))
    op.add_column('tb_teacher', sa.Column('sign_number', sa.String(length=4), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tb_teacher', 'sign_number')
    op.drop_column('tb_student', 'sign_times')
    # ### end Alembic commands ###

"""empty message

Revision ID: 950d611eee19
Revises: 3e68d99e73bf
Create Date: 2020-02-16 23:47:45.271726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '950d611eee19'
down_revision = '3e68d99e73bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_teacher',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=5), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('hash_password', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_teacher')
    # ### end Alembic commands ###

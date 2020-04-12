"""'1'

Revision ID: d3b3333107ad
Revises: a72389254f17
Create Date: 2020-03-24 20:11:06.948560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3b3333107ad'
down_revision = 'a72389254f17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_inform',
    sa.Column('url', sa.String(length=128), nullable=False),
    sa.Column('teacher_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['tb_teacher.id'], ),
    sa.PrimaryKeyConstraint('url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_inform')
    # ### end Alembic commands ###
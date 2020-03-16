"""empty message

Revision ID: a72389254f17
Revises: a646bc997413
Create Date: 2020-03-15 09:51:56.150095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a72389254f17'
down_revision = 'a646bc997413'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_teacher', sa.Column('final_time', sa.String(length=16), nullable=True))
    op.add_column('tb_teacher', sa.Column('teacher_time', sa.String(length=16), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tb_teacher', 'teacher_time')
    op.drop_column('tb_teacher', 'final_time')
    # ### end Alembic commands ###

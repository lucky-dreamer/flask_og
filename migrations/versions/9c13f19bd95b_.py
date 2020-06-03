"""empty message

Revision ID: 9c13f19bd95b
Revises: cddad580d020
Create Date: 2020-05-23 13:52:30.934026

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9c13f19bd95b'
down_revision = 'cddad580d020'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_course',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('theme', sa.String(length=64), nullable=True),
    sa.Column('introduction', sa.Text(length=1000), nullable=True),
    sa.Column('contain', sa.Integer(), nullable=True),
    sa.Column('teacher_time', sa.String(length=16), nullable=True),
    sa.Column('final_time', sa.String(length=16), nullable=True),
    sa.Column('teacher_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['tb_teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('tb_teacher', 'contain')
    op.drop_column('tb_teacher', 'theme')
    op.drop_column('tb_teacher', 'teacher_time')
    op.drop_column('tb_teacher', 'introduction')
    op.drop_column('tb_teacher', 'final_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tb_teacher', sa.Column('final_time', mysql.VARCHAR(length=16), nullable=True))
    op.add_column('tb_teacher', sa.Column('introduction', mysql.TEXT(), nullable=True))
    op.add_column('tb_teacher', sa.Column('teacher_time', mysql.VARCHAR(length=16), nullable=True))
    op.add_column('tb_teacher', sa.Column('theme', mysql.VARCHAR(length=64), nullable=True))
    op.add_column('tb_teacher', sa.Column('contain', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_table('tb_course')
    # ### end Alembic commands ###

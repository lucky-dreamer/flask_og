"""empty message

Revision ID: 1dc0f2b335ff
Revises: 7c12e5e9fa92
Create Date: 2020-04-12 10:28:39.334103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dc0f2b335ff'
down_revision = '7c12e5e9fa92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_question',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('time', sa.String(length=16), nullable=True),
    sa.Column('content', sa.Text(length=1000), nullable=True),
    sa.Column('student_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['tb_student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tb_reply',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('time', sa.String(length=16), nullable=True),
    sa.Column('content', sa.Text(length=1000), nullable=True),
    sa.Column('person', sa.String(length=5), nullable=True),
    sa.Column('question_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['tb_question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_reply')
    op.drop_table('tb_question')
    # ### end Alembic commands ###

"""test Student and Class registration

Revision ID: 064987acba3f
Revises: e599dbe51387
Create Date: 2020-04-27 10:53:13.971197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '064987acba3f'
down_revision = 'e599dbe51387'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('registrations',
    sa.Column('std_id', sa.Integer(), nullable=True),
    sa.Column('cls_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cls_id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['std_id'], ['students.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registrations')
    op.drop_table('students')
    op.drop_table('classes')
    # ### end Alembic commands ###

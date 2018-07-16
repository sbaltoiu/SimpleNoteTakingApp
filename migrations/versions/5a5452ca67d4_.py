"""empty message

Revision ID: 5a5452ca67d4
Revises: d2e7b5582af1
Create Date: 2018-07-15 19:28:05.248828

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5a5452ca67d4'
down_revision = 'd2e7b5582af1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'notes_ibfk_1', 'notes', type_='foreignkey')
    op.create_foreign_key(None, 'notes', 'users', ['user_id'], ['id'])
    op.drop_column('notes', 'user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('user', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.create_foreign_key(u'notes_ibfk_1', 'notes', 'users', ['user'], ['id'])
    op.drop_column('notes', 'user_id')
    # ### end Alembic commands ###

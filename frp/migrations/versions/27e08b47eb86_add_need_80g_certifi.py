"""Add need_80g_certificate column to userinfo table

Revision ID: 27e08b47eb86
Revises: None
Create Date: 2014-10-06 17:29:24.769861

"""

# revision identifiers, used by Alembic.
revision = '27e08b47eb86'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('userinfo', sa.Column('need_80g_certificate', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('userinfo', 'need_80g_certificate')
    ### end Alembic commands ###

"""empty message

Revision ID: 595c70886d1d
Revises: e79fdfc8c943
Create Date: 2020-06-15 12:11:18.250978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '595c70886d1d'
down_revision = 'e79fdfc8c943'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('acnt_message', sa.String(length=20), nullable=True))
    op.add_column('customer', sa.Column('cust_message', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer', 'cust_message')
    op.drop_column('account', 'acnt_message')
    # ### end Alembic commands ###
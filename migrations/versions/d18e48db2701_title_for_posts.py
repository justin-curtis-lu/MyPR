"""title for posts

Revision ID: d18e48db2701
Revises: 16bab3ae886e
Create Date: 2021-05-16 12:41:08.696816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd18e48db2701'
down_revision = '16bab3ae886e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('img')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img', sa.VARCHAR(length=140), nullable=True))

    # ### end Alembic commands ###

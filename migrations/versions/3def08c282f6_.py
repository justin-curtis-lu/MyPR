"""empty message

Revision ID: 3def08c282f6
Revises: d18e48db2701
Create Date: 2021-05-17 14:53:51.770029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3def08c282f6'
down_revision = 'd18e48db2701'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('img', sa.String(length=250), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('img')

    # ### end Alembic commands ###

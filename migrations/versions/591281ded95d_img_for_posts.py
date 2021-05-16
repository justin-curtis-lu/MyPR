"""img for posts

Revision ID: 591281ded95d
Revises: fe9710af6d8f
Create Date: 2021-05-15 15:45:22.499398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '591281ded95d'
down_revision = 'fe9710af6d8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('img', sa.String(length=140), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'img')
    # ### end Alembic commands ###

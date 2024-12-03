"""removed rating from users and service_req

Revision ID: 64afeda30899
Revises: 6f9b973d70ad
Create Date: 2024-12-03 20:35:18.829267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64afeda30899'
down_revision = '6f9b973d70ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('service_requests', schema=None) as batch_op:
        batch_op.drop_column('rating')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('rating')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.FLOAT(), nullable=True))

    with op.batch_alter_table('service_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.FLOAT(), nullable=True))

    # ### end Alembic commands ###

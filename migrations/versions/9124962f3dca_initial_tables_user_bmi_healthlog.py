"""Initial tables: User, BMI, HealthLog

Revision ID: 9124962f3dca
Revises: 05736381890a
Create Date: 2025-04-26 18:08:52.614838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9124962f3dca'
down_revision = '05736381890a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('gender')
        batch_op.drop_column('weight')
        batch_op.drop_column('age')
        batch_op.drop_column('height')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('height', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('weight', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('gender', sa.VARCHAR(length=10), autoincrement=False, nullable=False))

    # ### end Alembic commands ###

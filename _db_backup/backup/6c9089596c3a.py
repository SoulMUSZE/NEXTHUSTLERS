"""empty message

Revision ID: 6c9089596c3a
Revises: f0aa406d13a5
Create Date: 2019-05-27 17:37:34.543614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c9089596c3a'
down_revision = 'f0aa406d13a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hashtag_usage', sa.Column('id', sa.Integer(), nullable=False))
    op.alter_column('hashtag_usage', 'hashtag_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('hashtag_usage', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hashtag_usage', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('hashtag_usage', 'hashtag_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('hashtag_usage', 'id')
    # ### end Alembic commands ###

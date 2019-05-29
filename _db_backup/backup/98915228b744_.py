"""empty message

Revision ID: 98915228b744
Revises: a789fe99bc7a
Create Date: 2019-05-27 19:24:35.250667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98915228b744'
down_revision = 'a789fe99bc7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('hashtag_usage', 'hashtag_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('hashtag_usage', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'hashtag_usage', 'hashtag', ['hashtag_id'], ['id'])
    op.drop_column('hashtag_usage', 'created_at')
    op.drop_column('hashtag_usage', 'id')
    op.drop_column('hashtag_usage', 'updated_at')

    # with op.batch_alter_table('hashtag_usage') as batch_op:
    #     batch_op.drop_column('hashtag_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hashtag_usage', sa.Column('updated_at', sa.DATETIME(), nullable=True))
    op.add_column('hashtag_usage', sa.Column('id', sa.INTEGER(), nullable=False))
    op.add_column('hashtag_usage', sa.Column('created_at', sa.DATETIME(), nullable=True))
    op.drop_constraint(None, 'hashtag_usage', type_='foreignkey')
    op.alter_column('hashtag_usage', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('hashtag_usage', 'hashtag_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###

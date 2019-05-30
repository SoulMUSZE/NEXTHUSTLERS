"""empty message

Revision ID: 8be54f1756a7
Revises: 2debcbc38009
Create Date: 2019-05-28 17:31:04.414638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8be54f1756a7'
down_revision = '2debcbc38009'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hashtag')
    op.add_column('hashtag_usage', sa.Column('hashtag', sa.String(length=30), nullable=False))
    op.drop_constraint(None, 'hashtag_usage', type_='foreignkey')
    op.drop_column('hashtag_usage', 'hashtag_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hashtag_usage', sa.Column('hashtag_id', sa.INTEGER(), nullable=False))
    op.create_foreign_key(None, 'hashtag_usage', 'hashtag', ['hashtag_id'], ['id'])
    op.drop_column('hashtag_usage', 'hashtag')
    op.create_table('hashtag',
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('hashtag_name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('count', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
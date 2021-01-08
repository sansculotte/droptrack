"""user table

Revision ID: 0823eca8a7e1
Revises:
Create Date: 2021-01-08 17:37:21.934115

"""
from alembic import op
from webapp.type_decorators import Password
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0823eca8a7e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password', Password(length=166), nullable=True),
    sa.Column('api_key', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_api'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
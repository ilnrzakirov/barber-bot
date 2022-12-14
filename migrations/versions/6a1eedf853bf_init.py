"""init

Revision ID: 6a1eedf853bf
Revises: 
Create Date: 2022-10-01 15:08:15.951371

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '6a1eedf853bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'hair_days',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('master_name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('open', sa.Integer(), nullable=False),
        sa.Column('close', sa.Integer(), nullable=False),
        sa.Column('dinner', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'master',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.VARCHAR(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('master')
    op.drop_table('hair_days')
    # ### end Alembic commands ###

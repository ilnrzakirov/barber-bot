"""

Revision ID: a7160f6ea833
Revises: b9cd500884ec
Create Date: 2022-10-04 19:17:36.649516

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a7160f6ea833'
down_revision = 'b9cd500884ec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('records', sa.Column('date', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('records', 'date')
    # ### end Alembic commands ###
"""create table orders

Revision ID: fff8d2b20a3e
Revises:
Create Date: 2022-08-02 20:51:41.244266

"""

import sqlalchemy as sa
from alembic import op

revision = 'fff8d2b20a3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'orders',
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('order_number', sa.Integer(), nullable=False),
        sa.Column('amount_usd', sa.DECIMAL(), nullable=False),
        sa.Column('amount_rub', sa.DECIMAL(), nullable=False),
        sa.Column('delivery_date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('order_id'),
    )


def downgrade() -> None:
    op.drop_table('orders')

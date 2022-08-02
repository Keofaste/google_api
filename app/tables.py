
import sqlalchemy as sa

from app.db import Base


class Order(Base):
    __tablename__ = 'orders'

    order_id = sa.Column(sa.Integer, primary_key=True)
    order_number = sa.Column(sa.Integer, nullable=False)
    amount_usd = sa.Column(sa.DECIMAL, nullable=False)
    amount_rub = sa.Column(sa.DECIMAL, nullable=False)
    delivery_date = sa.Column(sa.Date, nullable=False)

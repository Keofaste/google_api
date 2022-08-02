import datetime
from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError
from pydantic import validator


class Order(BaseModel):
    order_id: int = Field(description='№', gt=0)
    order_number: int = Field(description='заказ №', gt=0)
    amount_usd: Decimal = Field(description='стоимость,$', gt=0)
    amount_rub: Decimal = Field(
        description='стоимость в руб.',
        gt=0,
        default=None,
    )
    delivery_date: datetime.date = Field(description='срок поставки')

    @validator('delivery_date', pre=True)
    def parse_delivery_date(cls, value) -> datetime.date:
        match value:
            case str():
                return datetime.datetime.strptime(value, '%d.%m.%Y').date()
            case datetime.date():
                return value
            case datetime.datetime():
                return value.date()
            case _:
                raise ValidationError("Can't validate delivery date")

    class Config:
        orm_mode = True

import datetime
from decimal import Decimal

import pytest

from app.services.cbr import CBRService


@pytest.fixture
def cbr_service() -> CBRService:
    return CBRService()


@pytest.mark.parametrize(
    argnames=['date', 'rate'],
    argvalues=[
        (datetime.date(2022, 2, 1), Decimal('77.4702')),
        (datetime.date(2021, 12, 31), Decimal('74.2926')),
        (datetime.date(2022, 1, 1), Decimal('74.2926')),
    ],
)
def test_get_usd_rate(
        cbr_service: CBRService,
        date: datetime.date,
        rate: Decimal,
):
    assert cbr_service.get_usd_rate(date=date) == rate

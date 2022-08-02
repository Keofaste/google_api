from datetime import datetime
from decimal import Decimal
from xml.etree import ElementTree

import requests

from app.settings import settings


class CBRRatesUnavailable(Exception):
    ...


class CBRService:
    """Сервис для получения курса доллара США по ЦБ РФ на заданную дату"""

    usd_rates: dict[datetime.date, Decimal]

    def __init__(self):
        self.usd_rates = {}

    def get_usd_rate(self, date: datetime.date) -> Decimal:
        if date not in self.usd_rates:
            self.usd_rates[date] = self._retrieve_usd_rate_from_cbr(date)

        return self.usd_rates[date]

    def _retrieve_usd_rate_from_cbr(self, date: datetime.date) -> Decimal:
        url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(
            date.strftime('%d/%m/%Y'),
        )
        # тут столо бы добавить логирование ошибок и повторение запроса
        # (если ошибка не из-за слишком частых запросов, конечно)
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException:
            raise CBRRatesUnavailable()

        if response.status_code != 200:
            raise CBRRatesUnavailable(
                f'response status code "{response.status_code}"',
            )

        tree = ElementTree.fromstring(response.text)
        rate_node = tree.find(f".//*[@ID='{settings.usd_code}']/Value")
        if rate_node is not None:
            return Decimal(rate_node.text.replace(',', '.'))

        raise CBRRatesUnavailable('rate not found')

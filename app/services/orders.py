import logging
from decimal import Decimal
from enum import Enum
from enum import auto
from enum import unique

import gspread
from gspread import Client
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import tables
from app.models import Order
from app.services.cbr import CBRService
from app.settings import settings

logger = logging.getLogger()


@unique
class OrderColumns(Enum):
    ID = 0
    NUMBER = auto()
    AMOUNT_USD = auto()
    DELIVERY_DATE = auto()


class OrdersService:
    _google_client: Client = None
    _db_session: Session = None
    _cbr_service: CBRService = None

    def __init__(self, session: Session):
        self._google_client = gspread.service_account('./service_account.json')
        self._db_session = session
        self._cbr_service = CBRService()

    def update_orders_from_google_sheet(self):
        order_ids: list[int] = []
        for order in self._retrieve_orders():
            # Тут получение стоимости в рублях сделано не оптимально.
            # Лучше сначала проверять изменилась ли дата либо сумма USD,
            # и только потом получать новое значение.
            order.amount_rub = self._get_order_amount_rub(order)
            self._sync_to_db(order)
            order_ids.append(order.order_id)

        # Удаляем записи, которые есть в БД, но нет в гугл-таблице
        self._cleanup_old_orders(order_ids)

    def _retrieve_orders(self) -> list[Order]:
        spreadsheet = self._google_client.open_by_key(
            key=settings.google_sheet_key,
        )
        worksheet = spreadsheet.get_worksheet(0)

        # Тут можно добавить проверку был ли изменена гугл-таблица после
        # последнего обращения к ней.
        # Если нет, то и обновлять записи в БД смысла нет.

        orders = []
        # пропускаем заголовок таблицы
        for row in worksheet.get_values('A2:D'):
            try:
                orders.append(Order(
                    order_id=row[OrderColumns.ID.value],
                    order_number=row[OrderColumns.NUMBER.value],
                    amount_usd=row[OrderColumns.AMOUNT_USD.value],
                    delivery_date=row[OrderColumns.DELIVERY_DATE.value],
                ))
            except ValidationError:
                # Получили доступ к записи в момент создания/редактирования,
                # пропускаем. Если повторяется, возможно стоит отправлять
                # уведомление заинтересованным лицам
                logger.warning(f'ошибка парсинга заказа: {row}')
                continue
        return orders

    def _sync_to_db(self, order_data: Order) -> tables.Order:
        """Создаёт новую запись, если заказ отсутствует в БД,
        либо обновляет существующую запись.
        """
        order = self._db_session.query(tables.Order).get(order_data.order_id)
        if order is None:
            order = tables.Order(**order_data.dict())
            self._db_session.add(order)
        else:
            for field, value in order_data:
                setattr(order, field, value)

        self._db_session.commit()
        return order

    def _get_order_amount_rub(self, order: Order) -> Decimal:
        rate = self._cbr_service.get_usd_rate(order.delivery_date)
        return round(order.amount_usd * rate, 2)

    def _cleanup_old_orders(self, order_ids_to_save: list[int]):
        """Очистка заказов, которые не присутствуют в гугл-таблице"""
        self._db_session.query(tables.Order).filter(
            tables.Order.order_id.not_in(order_ids_to_save),
        ).delete()
        self._db_session.commit()

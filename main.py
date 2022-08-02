from time import sleep

from app.db import SessionManager
from app.services.orders import OrdersService


def main():
    with SessionManager() as sm:
        service = OrdersService(session=sm.session)
        while True:
            service.update_orders_from_google_sheet()
            # таймаут в пять секунд исключительно чтобы не тратить
            # слишком много запросов к апи гугла
            sleep(5)


if __name__ == "__main__":
    main()

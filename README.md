# Тестовое задание на позицию test 'Backend developer (Python)'

## Задание
Необходимо разработать скрипт на языке Python 3, 
который будет выполнять следующие функции:

1. Получать данные с документа при помощи Google API, 
сделанного в [Google Sheets](https://docs.google.com/spreadsheets/d/1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g/edit) (необходимо копировать в свой Google аккаунт и выдать самому себе права).
2. Данные должны добавляться в БД, в том же виде, что и в файле–источнике,
с добавлением колонки «стоимость в руб.»
   1. Необходимо создать DB самостоятельно, СУБД на основе PostgreSQL.
   2. Данные для перевода $ в рубли необходимо получать по курсу [ЦБ РФ](https://www.cbr.ru/development/SXML/).
    
3. Скрипт работает постоянно для обеспечения обновления данных в онлайн режиме
(необходимо учитывать, что строки в Google Sheets таблицу могут удаляться,
добавляться и изменяться).

Дополнения, которые дадут дополнительные баллы и поднимут потенциальный уровень
оплаты труда:
1. Упаковка решения в docker контейнер 
2. Разработка функционала проверки соблюдения «срока поставки» из таблицы.
В случае, если срок прошел, скрипт отправляет уведомление в Telegram.
3. Разработка одностраничного web-приложения на основе Django или Flask.
Front-end React.

## Как запустить

1. Положить json-файл приватного ключа от сервисного гугл-аккаунта, 
в корень проекта и переименовать в `service_account.json`
2. Создать env файлы в директории envs (там же есть шаблоны)
3. Предоставить доступ сервисному аккаунту к гугл-таблице, id которой указан 
в `envs/app.env`
4. `make build`
5. `make run`
6. `make stop` для остановки

[гугл док](https://docs.google.com/spreadsheets/d/1DfW6GIH39ljIz0hcZnEYeHV0O5H_8VNLOg2DdEd3l58/edit)

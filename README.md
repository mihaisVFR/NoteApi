## Развертывание на локальной машине
1. Установить pipenv sudo apt update, apt install pipenv
2. Создать виртуальное окружение и установить зависимости: pipenv sync
3.  Запустить виртуальное окружение: pipenv shell
4. Миграции, Создание локальной БД flask db init,flask db migrate -m "new db"",flask db upgrade

## Автотесты
1. Запуск: pytest -v tests

## Реализовано ТЗ

### Основные возможности:

- [x] Регистрация пользователя.
- [x] Авторизация пользователя.
- [x] Создание заметки. Каждая заметка привязывается к конкретному пользователю. 
  Без регистрации нельзя создавать заметки.

- [x] Просмотр своих заметок.
- [x] Просмотр публичных заметок других пользователей.
  При создании заметки пользователь может указать для нее статус “публичная”,
  тогда данная заметка будет видна всем прочим пользователям.
  По умолчанию статус заметки “частная”.

- [x] Редактирование собственных заметок. Изменение текста заметки и ее статуса(публичная/частная).
- [x] Удаление собственных заметок.

### Дополнительные возможности:

- [x] Создание списка категорий 
- [x] Добавление категорий заметке.
- [x] Получение заметок по определенным категориям. 

## Полезное
1. Статья о связях many-to-many в flask sqlalchemy https://ploshadka.net/sqlalchemy-many-to-many/
2. Коллекция запросов Postman находится в дирректории PosnmanCollection
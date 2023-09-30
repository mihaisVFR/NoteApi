# Развертывание на локальной машине
1. Установить pipenv sudo apt update, apt install pipenv
2. Создать виртуальное окружение и установить зависимости: pipenv sync
3.  Запустить виртуальное окружение: pipenv shell
4. Миграции, Создание локальной БД flask db init,flask db migrate -m "new db"",flask db upgrade

# Автотесты
1. Запуск: pytest -v tests
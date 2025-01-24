***Установка

1. Клонировать репозиторий
    git clone <repository>
2. Установить зависимости из файла requirements.txt
3. Создать БД и указать данные от нее в файле .env. Приложение было настроено под работу с PostgreSQL
    DB_HOST = #localhost
    DB_PORT = #5432 default
    DB_USER = #user
    DB_PASS = #pass
    DB_NAME = #name
4. Выполнить миграции для БД
    python manage.py makemigrations
    python manage.py migrate
5. Запустить веб сервер
    python manage.py runserver


***Взаимодействие с проектом

Работать с приложением можно в 2 форматах:
1. API
    Для работы с API требуется перейти на http://localhost:8000/api
2. HTML интерфейс
    Для работы с HTML страницами требуется перейти на http://localhost:8000/

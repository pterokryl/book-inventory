# Book Inventory

Простой сервис учета книг на Django.

## Что есть в проекте

- Поля книги: автор, название, год издания, помещение, шкаф, полка, фото.
- Список книг.
- Поиск по всем полям.
- Фильтры по каждому полю.
- Добавление и редактирование книги.
- Локальная БД SQLite по умолчанию.
- Поддержка облачной PostgreSQL через `DATABASE_URL`.

## Локальный запуск

1. Установите Python 3.11+.
2. В корне проекта:
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
   - `pip install -r requirements.txt`
3. Выполните миграции:
   - `python manage.py migrate`
4. Запустите сервер:
   - `python manage.py runserver`
5. Откройте:
   - `http://127.0.0.1:8000/`

## Интеграция с облачной БД (Neon, пошагово)

1. Создайте аккаунт на [Neon](https://neon.tech/) и новый Project.
2. В Neon откройте раздел подключения и скопируйте строку подключения в формате:
   - `postgresql://user:password@host/dbname?sslmode=require`
3. В корне проекта создайте файл `.env` на основе `.env.example`.
4. В `.env` заполните:
   - `DATABASE_URL=<ваша строка из Neon>`
   - `DJANGO_DEBUG=True` (для локальной разработки)
   - `DJANGO_SECRET_KEY=<ваш ключ>`
5. Убедитесь, что установлены зависимости:
   - `pip install -r requirements.txt`
6. Примените миграции уже в облачную БД:
   - `python manage.py migrate`
7. Проверьте работу сервиса в браузере.

## Дальше для продакшена

- Поменять `DJANGO_DEBUG=False`.
- Настроить `DJANGO_ALLOWED_HOSTS`.
- Подключить статику и медиа в объектное хранилище (например, S3-совместимое).

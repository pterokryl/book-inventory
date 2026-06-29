# Фото книг через Yandex Object Storage

В serverless-контейнере локальные файлы (`/tmp/media`) не видны между экземплярами.
Для фото используется Yandex Object Storage (S3-совместимое хранилище).

## 1) Создать бакет

1. Yandex Cloud Console -> **Object Storage** -> **Создать бакет**
2. Имя, например: `book-inventory-media`
3. Доступ: **Публичный** (чтение объектов) или настройте ACL `public-read` на объектах
4. Создать бакет

## 2) Создать ключ доступа

1. **Сервисные аккаунты** -> ваш аккаунт (или новый)
2. Роль на бакет/папку: `storage.editor` (или `storage.admin`)
3. **Создать статический ключ доступа** -> сохраните:
   - `Key ID` -> `AWS_ACCESS_KEY_ID`
   - `Secret` -> `AWS_SECRET_ACCESS_KEY`

## 3) Добавить GitHub Secrets

| Secret | Пример |
|--------|--------|
| `AWS_ACCESS_KEY_ID` | идентификатор ключа |
| `AWS_SECRET_ACCESS_KEY` | секрет ключа |
| `AWS_STORAGE_BUCKET_NAME` | `book-inventory-media` |
| `AWS_S3_ENDPOINT_URL` | `https://storage.yandexcloud.net` |
| `MEDIA_URL` | `https://storage.yandexcloud.net/book-inventory-media/media/` |

## 4) Передеплой

GitHub Actions -> **Run workflow**

## 5) Проверка

1. Добавьте книгу с фото
2. В списке должна открыться картинка по URL вида:
   `https://storage.yandexcloud.net/<bucket>/media/book_photos/...`

Старые фото, загруженные до подключения S3, нужно загрузить заново.

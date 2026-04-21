# Деплой в Yandex Cloud Container

Ниже пошаговый сценарий для деплоя Django-приложения в Serverless Containers.

## 1) Подготовка

- Установите и авторизуйте `yc` CLI.
- Убедитесь, что у вас есть:
  - `FOLDER_ID`
  - `REGISTRY_ID`
  - `SERVICE_ACCOUNT_ID` (с правами на запуск контейнера и чтение секрета)

## 2) Собрать и отправить образ в Container Registry

Пример (выполнять в корне проекта):

```bash
docker build -t cr.yandex/<registry_id>/book-inventory:latest .
docker push cr.yandex/<registry_id>/book-inventory:latest
```

Если Docker не авторизован в реестре:

```bash
yc container registry configure-docker
```

## 3) Создать контейнер (один раз)

```bash
yc serverless container create \
  --name book-inventory \
  --folder-id <folder_id>
```

## 4) Задеплоить ревизию контейнера

```bash
yc serverless container revision deploy \
  --container-name book-inventory \
  --image cr.yandex/<registry_id>/book-inventory:latest \
  --cores 1 \
  --memory 512MB \
  --concurrency 10 \
  --execution-timeout 60s \
  --service-account-id <service_account_id> \
  --environment DJANGO_DEBUG=False \
  --environment DJANGO_SECRET_KEY='<strong-secret>' \
  --environment DJANGO_ALLOWED_HOSTS='<container-url-host>' \
  --environment DJANGO_CSRF_TRUSTED_ORIGINS='https://<container-url-host>' \
  --environment DATABASE_URL='<postgres-url>'
```

Важно:
- `<container-url-host>` это только хост без `https://` для `DJANGO_ALLOWED_HOSTS`.
- Для `DJANGO_CSRF_TRUSTED_ORIGINS` указывается полный origin с `https://`.
- Для production лучше использовать PostgreSQL (Managed PostgreSQL / Neon), не SQLite.

## 5) Проверка

- Получить URL контейнера:

```bash
yc serverless container get --name book-inventory --folder-id <folder_id>
```

- Откройте URL и проверьте:
  - `/` (список книг)
  - `/admin/`

## 6) Обновление версии приложения

1. Внести изменения в код.
2. Пересобрать и отправить новый образ с новым тегом.
3. Выполнить `yc serverless container revision deploy` с новым тегом.

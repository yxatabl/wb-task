# 🛍️ StoreAPI - Интернет-магазин (REST API)

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.0+-green?logo=django)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14+-red?logo=django)](https://django-rest-framework.org)
[![Docker](https://img.shields.io/badge/Docker-✓-blue?logo=docker)](https://docker.com)
[![JWT](https://img.shields.io/badge/Auth-JWT-orange?logo=json-web-tokens)](https://jwt.io)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

REST API для интернет-магазина с JWT-аутентификацией.

## Функциональные возможности

### Пользователи
- Авторизация (JWT токены)
- Пополнение баланса

### Товары
- Просмотр товаров
- Создание/редактирование/удаление товаров (только для администраторов)

### Корзина
- Добавление/удаление товаров
- Изменение количества товаров
- Просмотр текущей корзины

### Заказы
- Создание заказа из текущей корзины
- История заказов

## Технический стек

| Компонент | Технология |
|-----------|------------|
| **Язык** | Python 3.13 |
| **Фреймворк** | Django 6.0 |
| **API** | Django REST Framework |
| **База данных** | PostgreSQL |
| **Аутентификация** | JWT (Simple JWT) |
| **Документация API** | drf-spectacular (Swagger) |
| **Логирование** | Django logging |
| **Тестирование** | Django TestCase |

## Запуск проекта

1. **Склонируйте репозиторий**
   ```bash
   git clone https://github.com/yxatabl/wb-task
   cd wb-task
   ```
2. **Создайте файл .env и введите параметры**
   ```bash
   cp .env.example .env
   ```
    Переменные окружения:
    ```env
   # Django
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database ( PostgreSQL)
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=store_db
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=db
   DB_PORT=5432

   # JWT Settings
   JWT_ACCESS_TOKEN_MINUTES=60
   JWT_REFRESH_TOKEN_DAYS=1

   # Django Superuser
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=admin
    ```
3. **Запустите контейнеры**
   ```bash
   docker-compose up --build
   ```

## 📚 API Документация

После запуска проекта документация доступна по следующим адресам:

| Инструмент | URL |
|------------|-----|
| **Swagger UI** | http://localhost:8000/api/docs/ |
| **OpenAPI Schema** | http://localhost:8000/api/schema/ |

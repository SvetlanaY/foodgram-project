# Foodgram-project
## Дипломный проект — сайт «Продуктовый помощник».

Создано с помощью Django Framework.База данных на PostgreSQL.

Шаблоны страниц на HTML с использованием CSS и JavaScript.

Сайт был запущен на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn( в настоящее время срок аренды на сервере закончен и сайт не доступен)



### Описание:
Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Установка:
Для установки ПО необходимо 
1. Создать .env с переменными окружения:
    - DB_ENGINE
    - DB_NAME
    - DB_USER
    - DB_PASSWORD
    - DB_HOST
    - DB_PORT
    - POSTGRES_USER
    - POSTGRES_PASSWORD
2. docker-compose up
3. docker container ls 
4. docker exec -it <id_контейнера_web> bash
5. В контейнере web выполнить миграции, создать суперюзера и загрузить данные:
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py loaddata dump.json

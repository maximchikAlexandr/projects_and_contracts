# Projects and Contracts 
## О проекте

Это тестовое задание для стажировки в iCode

## Установка

**Установка с тестовыми параметрами БД**. Сделать исполняемым файл со скриптом 
 и запустить его:

```sh
chmod +x install.sh && ./install.sh
```

**Установка с рабочими параметрами БД**. Склонировать репозиторий с GitHub:

```sh
git clone https://github.com/maximchikAlexandr/projects_and_contracts.git
```

Создать файл '.env' в корневой директории:

```sh
cd job_manager/job_manager_proj/
nano .env
```

и заполнить его следующими переменными окружения:

```sh
# database parameters
POSTGRES_DB=your_database_name
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_database_password
DB_HOST=postgres_db
DB_PORT=5432
DB_OUT_PORT=5434
```

Создать и запустить докер контейнеры:

```sh
docker compose up -d
```

Применить миграции к базе данных

```sh
docker exec -it pc_app alembic upgrade head
```

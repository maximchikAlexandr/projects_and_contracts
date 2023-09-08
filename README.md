# Projects and Contracts 
## О проекте

Это тестовое задание для стажировки в iCode

## Установка

Склонировать репозиторий с GitHub:

```sh
git clone https://github.com/maximchikAlexandr/projects_and_contracts.git
```

Перейти в директорию с проектом

```sh
cd projects_and_contracts/
```


### Linux

**Установка с тестовыми параметрами БД**. Сделать исполняемым файл со скриптом 
 и запустить его:

```sh
chmod +x install.sh && ./install.sh
```

**Установка с рабочими параметрами БД**. Создать файл '.env' в корневой директории:

```sh
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
SQLALCHEMY_LOG_LEVEL=CRITICAL
```

Создать и запустить докер контейнеры:

```sh
docker compose up -d
```

Применить миграции к базе данных

```sh
docker exec -it pc_app alembic upgrade head
```

## Использование

Для подключения к приложению нужно войти в докер контейнер с приложением:

```sh
docker exec -it pc_app bash
```

Для выхода из приложения:

```sh
exit
```
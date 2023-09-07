#!/bin/bash

POSTGRES_DB="test_db"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="123456"
DB_HOST="postgres_db"
DB_PORT=5432
DB_OUT_PORT=5434

echo "POSTGRES_DB=$POSTGRES_DB" > .env
echo "POSTGRES_USER=$POSTGRES_USER" >> .env
echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> .env
echo "DB_HOST=$DB_HOST" >> .env
echo "DB_PORT=$DB_PORT" >> .env
echo "DB_OUT_PORT=$DB_OUT_PORT" >> .env

docker-compose up -d --build && \
docker exec -it pc_app alembic upgrade head

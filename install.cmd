set PPOSTGRES_DB="test_db"
set PPOSTGRES_USER="postgres"
set PPOSTGRES_PASSWORD="123456"
set PDB_HOST="postgres_db"
set PDB_PORT=5432
set PDB_OUT_PORT=5434
set PSQLALCHEMY_LOG_LEVEL="CRITICAL"

echo POSTGRES_DB=%POSTGRES_DB% > .env
echo POSTGRES_USER=%POSTGRES_USER% >> .env
echo POSTGRES_PASSWORD=%POSTGRES_PASSWORD% >> .env
echo DB_HOST=%DB_HOST% >> .env
echo DB_PORT=%DB_PORT% >> .env
echo DB_OUT_PORT=%DB_OUT_PORT% >> .env
echo SQLALCHEMY_LOG_LEVEL=%SQLALCHEMY_LOG_LEVEL% >> .env

docker-compose up -d --build && \
docker exec -it pc_app alembic upgrade head

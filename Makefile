APP = web
DB = postgres
EXEC = docker exec -it

.PHONY: tests
tests:
	${EXEC} ${APP} pytest tests

.PHONY: psql
psql:
	${EXEC} ${DB} psql -U admin -d auth-db -h postgres -p 5432 -W admin

.PHONY: shell
shell:
	${EXEC} ${APP} bash

.PHONY: makemigrations
makemigrations:
	${EXEC} ${APP} alembic revision --autogenerate -m "Initial tables"

.PHONY: migrate
migrate:
	${EXEC} ${APP} alembic upgrade head

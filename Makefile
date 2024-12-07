APP = app
DB = postgres
EXEC = docker exec -it

.PHONY: tests
tests:
	${EXEC} ${APP} pytest tests

.PHONY: psql
psql:
	${EXEC} ${DB} psql -U postgres -d postgres

.PHONY: shell
shell:
	${EXEC} ${APP} bash

.PHONY: migrations
migrations:
	${EXEC} ${APP} alembic revision --autogenerate -m "$(msg)"

.PHONY: migrate
migrate:
	${EXEC} ${APP} alembic upgrade head

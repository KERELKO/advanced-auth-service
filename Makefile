APP = app
DB = postgres
EXEC = docker exec -it

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


.PHONY: tests
tests:
	${EXEC} ${APP} pytest tests

.PHONY: test-authentication
test-authentication:
	${EXEC} ${APP} pytest tests/services/test_authentication.py

.PHONY: test-authorization
test-authorization:
	${EXEC} ${APP} pytest tests/services/test_authorization.py

.PHONY: test-mfa
test-mfa:
	${EXEC} ${APP} pytest tests/services/test_mfa.py

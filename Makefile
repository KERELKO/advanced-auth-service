.PHONY: tests
tests:
	docker exec -it web pytest tests

.PHONY: psql
psql:
	docker exec -it postgres psql -U postgres

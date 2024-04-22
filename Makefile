-include .env

build:
	docker compose build

up:
	docker compose up -d

down:
	docker-compose down

log:
	docker compose logs

python:
	docker exec -it $(PYTHON_CONTAINER_HOST) /bin/sh
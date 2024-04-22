-include .env

build:
	docker compose build

up:
	docker compose up -d

log:
	docker compose logs

python:
	docker exec -it $(PYTHON_CONTAINER_HOST) /bin/sh
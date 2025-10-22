run:
	docker-compose up

build:
	docker-compose up --build

stop:
	docker stop SITE_SERVER
	docker stop SITE_DB
	docker stop SITE_CELERY_BEAT
	docker stop SITE_CELERY
	docker stop SITE_REDIS

server-up:
	docker start SITE_SERVER

server-down:
	docker stop SITE_SERVER

db-up:
	docker start SITE_DB

db-down:
	docker stop SITE_DB

server-shell:
	docker exec -it SITE_SERVER /bin/bash

db-shell:
	docker exec -it SITE_DB /bin/bash

test: db-up server-up
	docker exec -it SITE_SERVER pytest --cov-fail-under=99
	docker stop SITE_SERVER
	docker stop SITE_DB

lint:
	docker exec -it SITE_SERVER isort .
	docker exec -it SITE_SERVER black .
	docker exec -it SITE_SERVER flake8 --exit-zero

all: test lint
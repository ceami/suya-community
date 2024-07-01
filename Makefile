.PHONY: run-server
run-server:
	poetry run uvicorn info_reels_docker.apps.app.main:app --host 0.0.0.0 --port 8080 --reload

.PHONY: build-dev
build-dev:
	docker-compose -f docker-compose.dev.yml build

.PHONY: up-dev
up-dev:
	docker-compose -f docker-compose.dev.yml up

.PHONY: build-up-dev
build-up-dev: build-dev up-dev

.PHONY: build-prod
build-prod:
	docker-compose -f docker-compose.prod.yml build

.PHONY: up-prod
up-prod:
	docker-compose -f docker-compose.prod.yml up

.PHONY: build-up-prod
build-up-prod: build-prod up-prod

.PHONY: push
push:
	docker-compose -f docker-compose.dev.yml build
	docker commit fastapi-projects-app-1 info_reels:1.0
	docker tag info_reels:1.0 creepereye/info_reels_2:1.0
	docker push creepereye/info_reels_2:1.0


.PHONY: help build up down logs migrate dev

help:
	@echo "Available commands:"
	@echo "  make build         - Build Docker images"
	@echo "  make up            - Start all services"
	@echo "  make down          - Stop all services"
	@echo "  make logs          - View service logs"
	@echo "  make logs-backend  - View backend logs"
	@echo "  make logs-db       - View database logs"
	@echo "  make migrate       - Run database migrations"
	@echo "  make dev           - Start services in development mode"
	@echo "  make clean         - Remove containers and volumes"

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-db:
	docker compose logs -f postgres

migrate:
	docker compose exec backend alembic upgrade head

dev:
	docker compose up --build

clean:
	docker compose down -v

.env:
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env from .env.example"; fi

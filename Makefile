# Image Classification Service - Development Commands

.PHONY: help build up down logs clean test lint format

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build all Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  logs      - View logs from all services"
	@echo "  clean     - Remove all containers, images, and volumes"
	@echo "  test      - Run tests for backend and frontend"
	@echo "  lint      - Run linting for backend and frontend"
	@echo "  format    - Format code for backend and frontend"
	@echo "  dev       - Start development environment"
	@echo "  prod      - Start production environment"
	@echo "  db-reset  - Reset database (DANGER: will delete all data)"

# Build all images
build:
	docker-compose build

# Start development environment
dev:
	docker-compose up -d database redis
	@echo "Waiting for database to be ready..."
	@sleep 10
	docker-compose up backend frontend

# Start all services
up:
	docker-compose up -d

# Start production environment with nginx
prod:
	docker-compose --profile production up -d

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# View logs for specific service
logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f database

# Clean up everything (DANGER: removes all data)
clean:
	docker-compose down -v --rmi all --remove-orphans
	docker system prune -f

# Reset database (DANGER: will delete all data)
db-reset:
	docker-compose stop database
	docker-compose rm -f database
	docker volume rm image-classification-service_postgres_data || true
	docker-compose up -d database
	@echo "Database reset complete"

# Run tests
test:
	@echo "Running backend tests..."
	docker-compose exec backend python -m pytest tests/ -v
	@echo "Running frontend tests..."
	docker-compose exec frontend npm run test

# Run linting
lint:
	@echo "Linting backend..."
	docker-compose exec backend python -m flake8 app/
	docker-compose exec backend python -m black --check app/
	@echo "Linting frontend..."
	docker-compose exec frontend npm run lint

# Format code
format:
	@echo "Formatting backend code..."
	docker-compose exec backend python -m black app/
	docker-compose exec backend python -m isort app/
	@echo "Formatting frontend code..."
	docker-compose exec frontend npm run format

# Install dependencies
install:
	@echo "Installing backend dependencies..."
	docker-compose exec backend pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	docker-compose exec frontend npm install

# Database operations
db-migrate:
	docker-compose exec backend alembic upgrade head

db-shell:
	docker-compose exec database psql -U postgres -d image_classification_db

# Quick commands for common operations
restart:
	docker-compose restart

status:
	docker-compose ps

# Development helpers
shell-backend:
	docker-compose exec backend bash

shell-frontend:
	docker-compose exec frontend sh

shell-db:
	docker-compose exec database bash

# Health check
health:
	@echo "Checking service health..."
	@curl -s http://localhost:8000/api/v1/health | jq . || echo "Backend not responding"
	@curl -s http://localhost:3000 > /dev/null && echo "Frontend is responding" || echo "Frontend not responding"
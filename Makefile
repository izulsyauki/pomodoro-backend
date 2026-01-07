.PHONY: install run dev migrate upgrade downgrade test clean help

# Variables
PYTHON = python3
PIP = pip3
UVICORN = uvicorn

help:
	@echo "Pomodoro API - Available Commands:"
	@echo ""
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run production server"
	@echo "  make dev        - Run development server with reload"
	@echo "  make migrate    - Create new migration"
	@echo "  make upgrade    - Apply all migrations"
	@echo "  make downgrade  - Rollback last migration"
	@echo "  make freeze     - Freeze requirements"
	@echo "  make clean      - Clean cache files"
	@echo "  make setup      - Initial setup (install + upgrade)"
	@echo ""

install:
	$(PIP) install -r requirements.txt

freeze:
	$(PIP) freeze > requirements.txt

run:
	$(UVICORN) app.main:app --host 0.0.0.0 --port 8000

dev:
	$(UVICORN) app.main:app --host 0.0.0.0 --port 8000 --reload

migrate:
	@read -p "Migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

setup: install upgrade
	@echo "Setup complete! Run 'make dev' to start the server."

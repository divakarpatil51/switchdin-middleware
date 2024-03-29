create-venv:
	poetry shell

install-poetry:
	pip install poetry

install-dependencies:
	poetry install

start-app:
	uvicorn src.main:app --reload

create-db-revision:
	alembic revision -m "$(MESSAGE)" --autogenerate

apply-migrations:
	alembic upgrade head

start-db:
	docker-compose up

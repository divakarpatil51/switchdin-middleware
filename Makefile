create-venv:
	poetry shell

install-poetry:
	pip install poetry

install-dependencies:
	poetry install

start-app:
	uvicorn src.main:app --reload

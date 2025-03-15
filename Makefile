.PHONY: setup format clean

DOCKERFILE := .docker/Dockerfile

setup:
	uv venv .venv
	. .venv/bin/activate && uv pip install -r requirements.txt

format:
	. .venv/bin/activate && ruff format
	. .venv/bin/activate && ruff check --fix

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

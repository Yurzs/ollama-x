DOCKERFILE := .docker/Dockerfile

format:
	@poetry run ruff format
	@poetry run ruff check --fix

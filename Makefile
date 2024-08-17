
DOCKERFILE := .docker/Dockerfile

publish:
	docker buildx build \
		-f $(DOCKERFILE) \
		--platform linux/amd64,linux/arm64 \
		-t ghcr.io/yurzs/ollama-x:latest \
		--push \
		.

format:
	@poetry run autoflake .
	@poetry run isort .
	@poetry run black .

FORMAT_PATH = zoopla_bridge functional_tests
OPENAPI_IGNORE_RULES = missing_amazon_integration,options_cors_not_enough_verbs

init:
	docker-compose build

start:
	docker-compose up web

test:
	docker-compose run --rm funtest pytest

lint:
	poetry run flake8
	poetry run aws-openapi-lint openapi/openapi.yaml --exclude-rules $(OPENAPI_IGNORE_RULES)

format:
	poetry run black $(FORMAT_PATH)
	poetry run isort .
	poetry run autoflake --remove-all-unused-imports --in-place --remove-unused-variables --recursive $(FORMAT_PATH)

setup:
	docker-compose run --rm web python -m zoopla_bridge.search_setup

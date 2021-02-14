SRC_DIR=ncbitax2lin
TESTS_DIR=tests

# https://www.gnu.org/software/make/manual/html_node/Force-Targets.html
FORCE:

format: FORCE
	poetry run autoflake --recursive --in-place --remove-all-unused-imports $(SRC_DIR) $(TESTS_DIR) \
	&& poetry run black $(SRC_DIR) $(TESTS_DIR) \
	&& poetry run isort $(SRC_DIR) $(TESTS_DIR) \

black: FORCE
	poetry run black --check $(SRC_DIR) $(TESTS_DIR)

isort: FORCE
	poetry run isort --check $(SRC_DIR) $(TESTS_DIR)

mypy: FORCE
	poetry run mypy $(SRC_DIR) $(TESTS_DIR)

pylint: FORCE
	poetry run pylint $(SRC_DIR) $(TESTS_DIR)

test: FORCE
	PYTHONHASHSEED=1 \
	&& poetry run coverage run --source=$(SRC_DIR) --module pytest --durations=10 --failed-first $(1) \
	&& poetry run coverage report --show-missing \
	&& poetry run coverage html

lint: black isort mypy pylint

all: lint pytest
